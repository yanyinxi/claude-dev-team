// =====================================================
// 监控系统 API 服务
// =====================================================
// 功能：封装监控中心的所有 API 请求
// 依赖：request.ts（Axios 封装）
// =====================================================

import request from './request'

// ==================== 类型定义 ====================

/**
 * 智能水平分数
 */
export interface IntelligenceScore {
  timestamp: string
  intelligence_score: number
  strategy_weight: number
  knowledge_richness: number
  quality_trend: number
  evolution_frequency: number
}

/**
 * 学习路径里程碑
 */
export interface Milestone {
  timestamp: string
  event: string
  intelligence_score: number
}

/**
 * 智能水平走势响应
 */
export interface IntelligenceTrendResponse {
  trend: IntelligenceScore[]
  milestones: Milestone[]
}

/**
 * 进化对比详情
 */
export interface EvolutionDiff {
  before: string
  after: string
  impact: string
}

/**
 * 进化事件
 */
export interface EvolutionEvent {
  id: string
  timestamp: string
  agent: string
  strategy: string
  description: string
  reward: number
  diff?: EvolutionDiff
}

/**
 * 进化事件流响应
 */
export interface EvolutionStreamResponse {
  total: number
  events: EvolutionEvent[]
}

/**
 * 诊断问题
 */
export interface DiagnosisIssue {
  id: string
  severity: 'Critical' | 'Important' | 'Suggestion'
  category: 'performance' | 'security' | 'quality' | 'architecture'
  title: string
  description: string
  location?: string
  suggestion?: string
  auto_fixable: boolean
  fix_code?: string
}

/**
 * 诊断响应
 */
export interface DiagnosisResponse {
  last_diagnosis_time: string
  next_diagnosis_time: string
  issues: DiagnosisIssue[]
}

/**
 * 修复变更
 */
export interface FixChange {
  file: string
  line: number
  before: string
  after: string
}

/**
 * 修复结果
 */
export interface FixResult {
  issue_id: string
  fixed: boolean
  changes: FixChange[]
}

/**
 * 性能指标
 */
export interface PerformanceMetrics {
  total_tasks: number
  success_rate: number
  avg_duration_seconds: number
  last_active?: string
}

/**
 * Agent 性能
 */
export interface AgentPerformance {
  name: string
  type: string
  current_progress: number
  status: 'working' | 'completed' | 'failed' | 'idle'
  performance: PerformanceMetrics
}

/**
 * 知识条目
 */
export interface KnowledgeItem {
  id: string
  title: string
  description: string
  source: string
  updated_at: string
  tags: string[]
}

/**
 * 知识分类
 */
export interface KnowledgeCategory {
  count: number
  items: KnowledgeItem[]
}

/**
 * 知识图谱响应
 */
export interface KnowledgeGraphResponse {
  categories: Record<string, KnowledgeCategory>
}

// ==================== API 方法 ====================

/**
 * 获取智能水平走势数据
 * @param days 时间范围（7/30/all）
 */
export async function getIntelligenceTrend(days: string = '7'): Promise<IntelligenceTrendResponse> {
  const response = await request.get(`/api/v1/monitor/intelligence-trend?days=${days}`)
  return response.data
}

/**
 * 获取进化事件流
 * @param limit 每页数量
 * @param offset 偏移量
 */
export async function getEvolutionStream(limit: number = 50, offset: number = 0): Promise<EvolutionStreamResponse> {
  const response = await request.get(`/api/v1/monitor/evolution-stream?limit=${limit}&offset=${offset}`)
  return response.data
}

/**
 * 获取智能诊断结果
 */
export async function getDiagnosis(): Promise<DiagnosisResponse> {
  const response = await request.get('/api/v1/monitor/diagnosis')
  return response.data
}

/**
 * 一键修复问题
 * @param issueId 问题 ID
 */
export async function fixIssue(issueId: string): Promise<FixResult> {
  const response = await request.post('/api/v1/monitor/diagnosis/fix', { issue_id: issueId })
  return response.data
}

/**
 * 获取 Agent 性能数据
 * @param type Agent 类型筛选
 */
export async function getAgentPerformance(type: string = 'all'): Promise<AgentPerformance[]> {
  const response = await request.get(`/api/v1/monitor/agents?type=${type}`)
  return response.data.agents
}

/**
 * 获取知识图谱数据
 * @param category 知识类型筛选
 * @param search 搜索关键词
 */
export async function getKnowledgeGraph(category: string = 'all', search: string = ''): Promise<KnowledgeGraphResponse> {
  const response = await request.get(`/api/v1/monitor/knowledge-graph?category=${category}&search=${search}`)
  return response.data
}

/**
 * 创建 WebSocket 连接
 * @param token JWT Token
 * @param onMessage 消息回调
 * @param onError 错误回调
 */
export function createWebSocket(
  token: string,
  onMessage: (event: EvolutionEvent) => void,
  onError?: (error: Event) => void
): WebSocket {
  const ws = new WebSocket(`ws://localhost:8000/ws/monitor/evolution?token=${token}`)

  ws.onopen = () => {
    console.log('[Monitor WebSocket] 连接成功')
    
    // 心跳保活（每 30 秒）
    setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)
    
    if (message.type === 'evolution_event') {
      onMessage(message.data)
    } else if (message.type === 'pong') {
      console.log('[Monitor WebSocket] 心跳响应')
    }
  }

  ws.onerror = (error) => {
    console.error('[Monitor WebSocket] 错误:', error)
    onError?.(error)
  }

  ws.onclose = () => {
    console.log('[Monitor WebSocket] 连接关闭')
  }

  return ws
}
