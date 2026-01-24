"""
监控系统 - API 路由

功能：
1. 智能水平走势 API
2. 进化事件流 API
3. 智能诊断 API
4. 一键修复 API
5. Agent 性能 API
6. 知识图谱 API
7. WebSocket 实时推送

路由前缀: /api/v1/monitor
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
import json

from models.monitor_schema import (
    IntelligenceTrendResponse,
    IntelligenceScore,
    Milestone,
    EvolutionStreamResponse,
    DiagnosisResponse,
    DiagnosisIssue,
    FixRequest,
    FixResult,
    AgentPerformanceResponse,
    KnowledgeGraphResponse
)
from services.monitor_intelligence import IntelligenceCalculator
from services.monitor_diagnosis import DiagnosisService
from services.monitor_service import MonitorService


# 创建路由器
router = APIRouter(prefix="/monitor", tags=["监控"])

# 初始化服务
intelligence_calculator = IntelligenceCalculator()
diagnosis_service = DiagnosisService()
monitor_service = MonitorService()


# ==================== WebSocket 连接管理器 ====================

class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # 连接已断开，标记移除
                disconnected.append(connection)

        # 移除断开的连接
        for conn in disconnected:
            self.disconnect(conn)


# 全局连接管理器
manager = ConnectionManager()


# ==================== REST API 接口 ====================

@router.get("/intelligence-trend", response_model=IntelligenceTrendResponse)
async def get_intelligence_trend(days: Optional[str] = Query("7", description="时间范围: 7/30/all")):
    """
    获取智能水平走势数据

    Args:
        days: 时间范围，默认 7 天，可选 7/30/all

    Returns:
        IntelligenceTrendResponse: 智能水平走势数据
    """
    try:
        # 计算当前智能水平
        current_score = intelligence_calculator.calculate_intelligence_score()

        # 模拟历史数据（实际应从数据库查询）
        # 这里简化处理，生成最近 7 天的数据
        trend_data = []
        days_count = 7 if days == "7" else (30 if days == "30" else 90)

        for i in range(days_count, 0, -1):
            timestamp = datetime.now() - timedelta(days=i)
            # 模拟历史分数（实际应从数据库查询）
            score_variation = (i % 3) * 0.1
            trend_data.append(IntelligenceScore(
                timestamp=timestamp,
                intelligence_score=max(current_score.intelligence_score - score_variation, 0),
                strategy_weight=max(current_score.strategy_weight - score_variation * 0.1, 0),
                knowledge_richness=max(current_score.knowledge_richness - score_variation * 0.1, 0),
                quality_trend=max(current_score.quality_trend - score_variation * 0.1, 0),
                evolution_frequency=max(current_score.evolution_frequency - score_variation * 0.1, 0)
            ))

        # 添加当前数据
        trend_data.append(current_score)

        # 识别里程碑
        milestones = intelligence_calculator.identify_milestones()

        return IntelligenceTrendResponse(
            trend=trend_data,
            milestones=milestones
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取智能水平走势失败: {str(e)}")


@router.get("/evolution-stream", response_model=EvolutionStreamResponse)
async def get_evolution_stream(
    limit: int = Query(50, description="每页数量"),
    offset: int = Query(0, description="偏移量")
):
    """
    获取进化事件流

    Args:
        limit: 每页数量，默认 50
        offset: 偏移量，默认 0

    Returns:
        EvolutionStreamResponse: 进化事件流数据
    """
    try:
        return await monitor_service.get_evolution_stream(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取进化事件流失败: {str(e)}")


@router.get("/diagnosis", response_model=DiagnosisResponse)
async def get_diagnosis():
    """
    获取智能诊断结果

    Returns:
        DiagnosisResponse: 诊断结果
    """
    try:
        # 执行诊断
        issues = await diagnosis_service.run_diagnosis()

        # 计算下次诊断时间（每小时执行一次）
        now = datetime.now()
        next_diagnosis_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        return DiagnosisResponse(
            last_diagnosis_time=now,
            next_diagnosis_time=next_diagnosis_time,
            issues=issues
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行诊断失败: {str(e)}")


@router.post("/diagnosis/fix", response_model=FixResult)
async def fix_issue(request: FixRequest):
    """
    一键修复问题

    Args:
        request: 修复请求（包含 issue_id）

    Returns:
        FixResult: 修复结果
    """
    try:
        # 先获取问题详情
        issues = await diagnosis_service.run_diagnosis()
        issue = next((i for i in issues if i.id == request.issue_id), None)

        if not issue:
            raise HTTPException(status_code=404, detail=f"问题不存在: {request.issue_id}")

        # 执行修复
        result = await diagnosis_service.auto_fix_issue(request.issue_id, issue)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修复失败: {str(e)}")


@router.get("/agents", response_model=AgentPerformanceResponse)
async def get_agents(agent_type: str = Query("all", description="Agent 类型筛选")):
    """
    获取 Agent 性能数据

    Args:
        agent_type: Agent 类型筛选，默认 all

    Returns:
        AgentPerformanceResponse: Agent 性能数据
    """
    try:
        agents = await monitor_service.get_agent_performance(agent_type=agent_type)
        return AgentPerformanceResponse(agents=agents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取 Agent 性能失败: {str(e)}")


@router.get("/knowledge-graph", response_model=KnowledgeGraphResponse)
async def get_knowledge_graph(
    category: str = Query("all", description="知识类型筛选"),
    search: str = Query("", description="搜索关键词")
):
    """
    获取知识图谱数据

    Args:
        category: 知识类型筛选，可选 strategy/best-practice/template/error-handling/all
        search: 搜索关键词

    Returns:
        KnowledgeGraphResponse: 知识图谱数据
    """
    try:
        return await monitor_service.get_knowledge_graph(category=category, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识图谱失败: {str(e)}")


# ==================== WebSocket 接口 ====================

@router.websocket("/ws/evolution")
async def websocket_evolution_stream(
    websocket: WebSocket,
    token: str = Query(..., description="JWT Token")
):
    """
    WebSocket 实时进化事件推送

    认证: 通过 URL 参数传递 JWT Token

    Args:
        websocket: WebSocket 连接
        token: JWT Token（实际应验证）
    """
    # TODO: 验证 Token
    # try:
    #     user = await verify_token(token)
    # except:
    #     await websocket.close(code=1008, reason="Unauthorized")
    #     return

    # 接受连接
    await manager.connect(websocket)

    try:
        while True:
            # 接收客户端消息（心跳）
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "ping":
                # 响应心跳
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket 错误: {e}")
        manager.disconnect(websocket)


# ==================== 辅助函数 ====================

async def broadcast_evolution_event(event: dict):
    """
    广播进化事件到所有 WebSocket 连接

    Args:
        event: 进化事件数据
    """
    await manager.broadcast({
        "type": "evolution_event",
        "data": event
    })
