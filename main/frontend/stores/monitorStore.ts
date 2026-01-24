// =====================================================
// 监控系统状态管理
// =====================================================
// 功能：管理监控中心的全局状态
// 依赖：Pinia、monitor.ts
// =====================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {
  IntelligenceTrendResponse,
  EvolutionEvent,
  DiagnosisResponse,
  AgentPerformance,
  KnowledgeGraphResponse
} from '@/services/monitor'

export const useMonitorStore = defineStore('monitor', () => {
  // ==================== 状态定义 ====================

  // 智能水平走势数据
  const intelligenceTrend = ref<IntelligenceTrendResponse | null>(null)

  // 进化事件列表
  const evolutionEvents = ref<EvolutionEvent[]>([])

  // 进化事件总数
  const evolutionTotal = ref(0)

  // 最新进化事件（用于实时推送）
  const latestEvent = ref<EvolutionEvent | null>(null)

  // 诊断结果
  const diagnosis = ref<DiagnosisResponse | null>(null)

  // Agent 性能数据
  const agentPerformance = ref<AgentPerformance[]>([])

  // 知识图谱数据
  const knowledgeGraph = ref<KnowledgeGraphResponse | null>(null)

  // 加载状态
  const loading = ref({
    intelligence: false,
    evolution: false,
    diagnosis: false,
    agents: false,
    knowledge: false
  })

  // WebSocket 连接状态
  const wsConnected = ref(false)

  // ==================== 计算属性 ====================

  /**
   * 当前智能水平分数
   */
  const currentIntelligenceScore = computed(() => {
    if (!intelligenceTrend.value || intelligenceTrend.value.trend.length === 0) {
      return 0
    }
    return intelligenceTrend.value.trend[intelligenceTrend.value.trend.length - 1].intelligence_score
  })

  /**
   * 按严重程度分组的诊断问题
   */
  const diagnosisIssuesBySeverity = computed(() => {
    if (!diagnosis.value) {
      return {
        Critical: [],
        Important: [],
        Suggestion: []
      }
    }

    return {
      Critical: diagnosis.value.issues.filter(i => i.severity === 'Critical'),
      Important: diagnosis.value.issues.filter(i => i.severity === 'Important'),
      Suggestion: diagnosis.value.issues.filter(i => i.severity === 'Suggestion')
    }
  })

  /**
   * 工作中的 Agent 数量
   */
  const workingAgentsCount = computed(() => {
    return agentPerformance.value.filter(a => a.status === 'working').length
  })

  // ==================== Actions ====================

  /**
   * 设置智能水平走势数据
   */
  function setIntelligenceTrend(data: IntelligenceTrendResponse) {
    intelligenceTrend.value = data
  }

  /**
   * 设置进化事件列表
   */
  function setEvolutionEvents(events: EvolutionEvent[], total: number) {
    evolutionEvents.value = events
    evolutionTotal.value = total
  }

  /**
   * 添加新的进化事件（实时推送）
   */
  function addEvolutionEvent(event: EvolutionEvent) {
    evolutionEvents.value.unshift(event)
    evolutionTotal.value += 1
    latestEvent.value = event
  }

  /**
   * 设置诊断结果
   */
  function setDiagnosis(data: DiagnosisResponse) {
    diagnosis.value = data
  }

  /**
   * 移除已修复的问题
   */
  function removeFixedIssue(issueId: string) {
    if (diagnosis.value) {
      diagnosis.value.issues = diagnosis.value.issues.filter(i => i.id !== issueId)
    }
  }

  /**
   * 设置 Agent 性能数据
   */
  function setAgentPerformance(agents: AgentPerformance[]) {
    agentPerformance.value = agents
  }

  /**
   * 设置知识图谱数据
   */
  function setKnowledgeGraph(data: KnowledgeGraphResponse) {
    knowledgeGraph.value = data
  }

  /**
   * 设置加载状态
   */
  function setLoading(key: keyof typeof loading.value, value: boolean) {
    loading.value[key] = value
  }

  /**
   * 设置 WebSocket 连接状态
   */
  function setWsConnected(connected: boolean) {
    wsConnected.value = connected
  }

  /**
   * 重置所有状态
   */
  function reset() {
    intelligenceTrend.value = null
    evolutionEvents.value = []
    evolutionTotal.value = 0
    latestEvent.value = null
    diagnosis.value = null
    agentPerformance.value = []
    knowledgeGraph.value = null
    loading.value = {
      intelligence: false,
      evolution: false,
      diagnosis: false,
      agents: false,
      knowledge: false
    }
    wsConnected.value = false
  }

  return {
    // 状态
    intelligenceTrend,
    evolutionEvents,
    evolutionTotal,
    latestEvent,
    diagnosis,
    agentPerformance,
    knowledgeGraph,
    loading,
    wsConnected,

    // 计算属性
    currentIntelligenceScore,
    diagnosisIssuesBySeverity,
    workingAgentsCount,

    // Actions
    setIntelligenceTrend,
    setEvolutionEvents,
    addEvolutionEvent,
    setDiagnosis,
    removeFixedIssue,
    setAgentPerformance,
    setKnowledgeGraph,
    setLoading,
    setWsConnected,
    reset
  }
})
