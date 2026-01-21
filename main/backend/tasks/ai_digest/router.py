"""
AI 日报 API 路由

端点：
- GET /api/v1/ai-digest/latest - 获取最新日报
- GET /api/v1/ai-digest/:date - 获取指定日期日报
- GET /api/v1/ai-digest - 获取日报列表
- POST /api/v1/ai-digest - 创建日报
- PATCH /api/v1/ai-digest/:id - 更新日报
- DELETE /api/v1/ai-digest/:id - 删除日报
"""

from datetime import date as date_type
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    AiDigestCreate,
    AiDigestUpdate,
    AiDigestResponse,
    AiDigestListItem,
)
from .service import AiDigestService
from core.database import get_db

router = APIRouter(prefix="/api/v1/ai-digest", tags=["AI Digest"])


@router.get("/latest", response_model=AiDigestResponse)
async def get_latest_digest(db: AsyncSession = Depends(get_db)):
    """
    获取最新日报

    Returns:
        AiDigestResponse: 最新日报
    """
    digest = await AiDigestService.get_latest(db)
    if not digest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="暂无日报数据"
        )

    return digest.to_dict()


@router.get("/{target_date}", response_model=AiDigestResponse)
async def get_digest_by_date(
    target_date: date_type, db: AsyncSession = Depends(get_db)
):
    """
    获取指定日期的日报

    Args:
        target_date: 日期（格式：YYYY-MM-DD）

    Returns:
        AiDigestResponse: 日报数据
    """
    digest = await AiDigestService.get_by_date(db, target_date)
    if not digest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"未找到 {target_date} 的日报"
        )

    return digest.to_dict()


@router.get("", response_model=List[AiDigestListItem])
async def get_digest_list(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=100, description="返回数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取日报列表

    Args:
        skip: 跳过数量
        limit: 返回数量（最大 100）

    Returns:
        List[AiDigestListItem]: 日报列表
    """
    digests = await AiDigestService.get_list(db, skip=skip, limit=limit)
    return [
        {
            "id": d.id,
            "date": d.date,
            "title": d.title,
            "total_items": d.total_items,
            "created_at": d.created_at,
        }
        for d in digests
    ]


@router.post("", response_model=AiDigestResponse, status_code=status.HTTP_201_CREATED)
async def create_digest(data: AiDigestCreate, db: AsyncSession = Depends(get_db)):
    """
    创建日报

    Args:
        data: 日报数据

    Returns:
        AiDigestResponse: 创建的日报
    """
    try:
        digest = await AiDigestService.create(db, data)
        return digest.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{digest_id}", response_model=AiDigestResponse)
async def update_digest(
    digest_id: int, data: AiDigestUpdate, db: AsyncSession = Depends(get_db)
):
    """
    更新日报

    Args:
        digest_id: 日报 ID
        data: 更新数据

    Returns:
        AiDigestResponse: 更新后的日报
    """
    digest = await AiDigestService.update(db, digest_id, data)
    if not digest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到 ID 为 {digest_id} 的日报",
        )

    return digest.to_dict()


@router.delete("/{digest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_digest(digest_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除日报

    Args:
        digest_id: 日报 ID
    """
    success = await AiDigestService.delete(db, digest_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到 ID 为 {digest_id} 的日报",
        )
