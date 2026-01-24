"""
闹钟路由 - 学习闹钟 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.db import User
from models.schema import (
    AlarmRuleCreate,
    AlarmRuleUpdate,
    AlarmRuleResponse,
    AlarmStatusResponse,
    AlarmValidateResponse
)
from services.alarm_service import AlarmService

router = APIRouter(prefix="/alarm", tags=["闹钟"])


# ============ 学生端 API ============


@router.get("/status", response_model=AlarmStatusResponse)
async def get_alarm_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前学习状态

    返回：
    - session_type: studying/resting/idle
    - start_time: 开始时间
    - end_time: 结束时间
    - remaining_seconds: 剩余秒数
    - is_blocked: 是否被阻止操作
    - rule: 生效的规则
    """
    try:
        status = await AlarmService.get_current_status(current_user.id, db)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取状态失败: {str(e)}"
        )


@router.post("/start", response_model=AlarmStatusResponse)
async def start_alarm(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    开始学习

    业务流程：
    1. 获取生效的规则（个性化优先于全局）
    2. 创建 studying 会话
    3. 自动创建下一个 resting 会话
    4. 返回当前状态
    """
    try:
        # 开始学习会话
        await AlarmService.start_session(current_user.id, db)

        # 返回当前状态
        status = await AlarmService.get_current_status(current_user.id, db)
        return status
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"开始学习失败: {str(e)}"
        )


@router.get("/validate", response_model=AlarmValidateResponse)
async def validate_alarm(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    验证是否可以操作

    返回：
    - can_operate: 是否可以操作
    - reason: 不能操作的原因
    - remaining_seconds: 剩余休息秒数
    """
    try:
        validation = await AlarmService.validate_operation(current_user.id, db)
        return validation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证失败: {str(e)}"
        )


# ============ 管理员端 API ============


@router.get("/rules", response_model=list[AlarmRuleResponse])
async def get_all_rules(
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有规则（需要管理员权限）

    返回所有闹钟规则列表
    """
    try:
        rules = await AlarmService.get_all_rules(db)
        return [AlarmRuleResponse.model_validate(rule) for rule in rules]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取规则失败: {str(e)}"
        )


@router.post("/rules", response_model=AlarmRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_data: AlarmRuleCreate,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    创建规则（需要管理员权限）

    请求参数：
    - rule_type: global/personal
    - student_nickname: 学生昵称（个性化规则必填）
    - study_duration: 学习时长（分钟）
    - rest_duration: 休息时长（分钟）
    """
    try:
        rule = await AlarmService.create_rule(rule_data, db)
        return AlarmRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建规则失败: {str(e)}"
        )


@router.put("/rules/{rule_id}", response_model=AlarmRuleResponse)
async def update_rule(
    rule_id: int,
    rule_data: AlarmRuleUpdate,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    更新规则（需要管理员权限）

    请求参数：
    - study_duration: 学习时长（分钟）
    - rest_duration: 休息时长（分钟）
    - is_active: 是否启用
    """
    try:
        rule = await AlarmService.update_rule(rule_id, rule_data, db)
        return AlarmRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新规则失败: {str(e)}"
        )


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: int,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    删除规则（需要管理员权限）
    """
    try:
        await AlarmService.delete_rule(rule_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除规则失败: {str(e)}"
        )


@router.patch("/rules/{rule_id}/toggle", response_model=AlarmRuleResponse)
async def toggle_rule(
    rule_id: int,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    启用/禁用规则（需要管理员权限）

    切换规则的 is_active 状态
    """
    try:
        rule = await AlarmService.toggle_rule(rule_id, db)
        return AlarmRuleResponse.model_validate(rule)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"切换规则状态失败: {str(e)}"
        )
