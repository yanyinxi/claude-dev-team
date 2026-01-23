"""
AI 日报 Pydantic Schema

用于 API 请求和响应的数据验证
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AiDigestSummaryItem(BaseModel):
    """日报摘要项"""

    title: str = Field(..., description="资讯标题")
    url: str = Field(..., description="资讯链接")
    description: str = Field(..., description="简短描述")


class AiDigestContentCategory(BaseModel):
    """日报内容分类"""

    category: str = Field(..., description="分类名称")
    items: list = Field(default_factory=list, description="分类下的资讯列表")


class AiDigestCreate(BaseModel):
    """创建 AI 日报"""

    digest_date: date = Field(..., alias="date", description="日报日期")
    title: str = Field(..., description="日报标题")
    summary: List[AiDigestSummaryItem] = Field(..., description="今日要闻摘要")
    content: Dict[str, Any] = Field(..., description="完整日报内容（JSON 对象）")
    total_items: int = Field(default=0, description="资讯总数")

    model_config = {"populate_by_name": True}


class AiDigestUpdate(BaseModel):
    """更新 AI 日报"""

    title: Optional[str] = Field(None, description="日报标题")
    summary: Optional[List[AiDigestSummaryItem]] = Field(
        None, description="今日要闻摘要"
    )
    content: Optional[Dict[str, Any]] = Field(None, description="完整日报内容（JSON 对象）")
    total_items: Optional[int] = Field(None, description="资讯总数")


class AiDigestResponse(BaseModel):
    """AI 日报响应"""

    id: int = Field(..., description="日报 ID")
    digest_date: date = Field(..., alias="date", description="日报日期")
    title: str = Field(..., description="日报标题")
    summary: List[AiDigestSummaryItem] = Field(..., description="今日要闻摘要")
    content: Dict[str, Any] = Field(..., description="完整日报内容（JSON 对象）")
    total_items: int = Field(..., description="资讯总数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
        populate_by_name = True


class AiDigestListItem(BaseModel):
    """AI 日报列表项（简化版）"""

    id: int = Field(..., description="日报 ID")
    digest_date: date = Field(..., alias="date", description="日报日期")
    title: str = Field(..., description="日报标题")
    total_items: int = Field(..., description="资讯总数")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
        populate_by_name = True
