"""
认证路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.schema import StudentLoginRequest, AdminLoginRequest, LoginResponse
from services.auth_service import AuthService


router = APIRouter()


@router.post("/auth/login/student", response_model=LoginResponse)
async def student_login(
    request: StudentLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    学生登录
    通过昵称登录，如果昵称不存在则自动创建账号
    """
    return await AuthService.student_login(request, db)


@router.post("/auth/login/admin", response_model=LoginResponse)
async def admin_login(
    request: AdminLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    管理员登录
    通过用户名和密码登录
    """
    return await AuthService.admin_login(request, db)
