"""
监控系统 - Pydantic 数据模型

功能：
1. 智能水平相关模型
2. 进化事件相关模型
3. 诊断相关模型
4. Agent 性能相关模型
5. 知识图谱相关模型
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict


# ==================== 智能水平相关 ====================

class IntelligenceScore(BaseModel):
    """
    智能水平分数

    计算公式：
    intelligence_score = (
        strategy_weight * 0.3 +
        knowledge_richness * 0.25 +
        quality_trend * 0.25 +
        evolution_frequency * 0.2
    ) * 10
    """
    timestamp: datetime = Field(..., description="时间戳")
    intelligence_score: float = Field(..., ge=0, le=10, description="智能水平总分 (0-10)")
    strategy_weight: float = Field(..., ge=0, le=1, description="策略权重 (0-1)")
    knowledge_richness: float = Field(..., ge=0, le=1, description="知识丰富度 (0-1)")
    quality_trend: float = Field(..., ge=0, le=1, description="质量趋势 (0-1)")
    evolution_frequency: float = Field(..., ge=0, le=1, description="进化频率 (0-1)")


class Milestone(BaseModel):
    """学习路径里程碑"""
    timestamp: datetime = Field(..., description="时间戳")
    event: str = Field(..., description="里程碑事件描述")
    intelligence_score: float = Field(..., ge=0, le=10, description="当时的智能水平")


class IntelligenceTrendResponse(BaseModel):
    """智能水平走势响应"""
    trend: List[IntelligenceScore] = Field(..., description="智能水平历史数据")
    milestones: List[Milestone] = Field(default=[], description="学习路径里程碑")


# ==================== 进化事件相关 ====================

class EvolutionDiff(BaseModel):
    """进化对比详情"""
    before: str = Field(..., description="改进前的做法")
    after: str = Field(..., description="改进后的做法")
    impact: str = Field(..., description="改进带来的影响")


class EvolutionEvent(BaseModel):
    """进化事件"""
    id: str = Field(..., description="事件唯一标识")
    timestamp: datetime = Field(..., description="事件时间")
    agent: str = Field(..., description="Agent 名称")
    strategy: str = Field(..., description="策略类型")
    description: str = Field(..., description="事件描述")
    reward: float = Field(..., ge=0, le=10, description="奖励分数 (0-10)")
    diff: Optional[EvolutionDiff] = Field(None, description="进化对比详情")


class EvolutionStreamResponse(BaseModel):
    """进化事件流响应"""
    total: int = Field(..., description="总事件数")
    events: List[EvolutionEvent] = Field(..., description="事件列表")


# ==================== 诊断相关 ====================

class DiagnosisIssue(BaseModel):
    """诊断问题"""
    id: str = Field(..., description="问题唯一标识")
    severity: str = Field(..., description="严重程度: Critical/Important/Suggestion")
    category: str = Field(..., description="问题类型: performance/security/quality/architecture")
    title: str = Field(..., description="问题标题")
    description: str = Field(..., description="问题描述")
    location: Optional[str] = Field(None, description="文件位置 (file:line)")
    suggestion: Optional[str] = Field(None, description="修复建议")
    auto_fixable: bool = Field(False, description="是否可自动修复")
    fix_code: Optional[str] = Field(None, description="修复代码")


class DiagnosisResponse(BaseModel):
    """诊断响应"""
    last_diagnosis_time: datetime = Field(..., description="上次诊断时间")
    next_diagnosis_time: datetime = Field(..., description="下次诊断时间")
    issues: List[DiagnosisIssue] = Field(..., description="诊断问题列表")


class FixRequest(BaseModel):
    """修复请求"""
    issue_id: str = Field(..., description="问题 ID")


class FixChange(BaseModel):
    """修复变更"""
    file: str = Field(..., description="文件路径")
    line: int = Field(..., description="行号")
    before: str = Field(..., description="修复前的代码")
    after: str = Field(..., description="修复后的代码")


class FixResult(BaseModel):
    """修复结果"""
    issue_id: str = Field(..., description="问题 ID")
    fixed: bool = Field(..., description="是否修复成功")
    changes: List[FixChange] = Field(..., description="修复变更列表")


# ==================== Agent 性能相关 ====================

class PerformanceMetrics(BaseModel):
    """性能指标"""
    total_tasks: int = Field(..., description="总任务数")
    success_rate: float = Field(..., ge=0, le=1, description="成功率 (0-1)")
    avg_duration_seconds: int = Field(..., description="平均耗时（秒）")
    last_active: Optional[datetime] = Field(None, description="最后活跃时间")


class AgentPerformance(BaseModel):
    """Agent 性能"""
    name: str = Field(..., description="Agent 名称")
    type: str = Field(..., description="Agent 类型: developer/reviewer/tester/orchestrator")
    current_progress: int = Field(..., ge=0, le=100, description="当前进度 (0-100)")
    status: str = Field(..., description="状态: working/completed/failed/idle")
    performance: PerformanceMetrics = Field(..., description="性能指标")


class AgentPerformanceResponse(BaseModel):
    """Agent 性能响应"""
    agents: List[AgentPerformance] = Field(..., description="Agent 列表")


# ==================== 知识图谱相关 ====================

class KnowledgeItem(BaseModel):
    """知识条目"""
    id: str = Field(..., description="知识条目 ID")
    title: str = Field(..., description="标题")
    description: str = Field(..., description="描述")
    source: str = Field(..., description="来源文件路径")
    updated_at: datetime = Field(..., description="更新时间")
    tags: List[str] = Field(default=[], description="标签列表")


class KnowledgeCategory(BaseModel):
    """知识分类"""
    count: int = Field(..., description="条目数量")
    items: List[KnowledgeItem] = Field(..., description="知识条目列表")


class KnowledgeGraphResponse(BaseModel):
    """知识图谱响应"""
    categories: Dict[str, KnowledgeCategory] = Field(..., description="分类字典")
