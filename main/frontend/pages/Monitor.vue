<!-- =====================================================
监控系统主页面
=====================================================
功能：监控中心主页面，包含 5 个子组件
职责：布局管理、WebSocket 连接管理、全局状态初始化
===================================================== -->

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'
import { useUserStore } from '@/stores/userStore'
import {
  getIntelligenceTrend,
  getEvolutionStream,
  getDiagnosis,
  getAgentPerformance,
  getKnowledgeGraph,
  createWebSocket
} from '@/services/monitor'
import MonitorIntelligenceChart from '@/components/MonitorIntelligenceChart.vue'
import MonitorDiagnosis from '@/components/MonitorDiagnosis.vue'
import MonitorEvolutionStream from '@/components/MonitorEvolutionStream.vue'
import MonitorAgentProgress from '@/components/MonitorAgentProgress.vue'
import MonitorKnowledgeGraph from '@/components/MonitorKnowledgeGraph.vue'

// ==================== 状态管理 ====================

const monitorStore = useMonitorStore()
const userStore = useUserStore()

// WebSocket 连接
const ws = ref<WebSocket | null>(null)

// 刷新状态
const refreshing = ref(false)

// ==================== 生命周期 ====================

onMounted(async () => {
  // 初始化数据
  await loadAllData()

  // 建立 WebSocket 连接
  connectWebSocket()
})

onUnmounted(() => {
  // 断开 WebSocket 连接
  if (ws.value) {
    ws.value.close()
  }
})

// ==================== 方法 ====================

/**
 * 加载所有数据
 */
async function loadAllData() {
  try {
    // 并行加载所有数据
    await Promise.all([
      loadIntelligenceTrend(),
      loadEvolutionStream(),
      loadDiagnosis(),
      loadAgentPerformance(),
      loadKnowledgeGraph()
    ])
  } catch (error) {
    console.error('[Monitor] 加载数据失败:', error)
  }
}

/**
 * 加载智能水平走势
 */
async function loadIntelligenceTrend() {
  monitorStore.setLoading('intelligence', true)
  try {
    const data = await getIntelligenceTrend('7')
    monitorStore.setIntelligenceTrend(data)
  } finally {
    monitorStore.setLoading('intelligence', false)
  }
}

/**
 * 加载进化事件流
 */
async function loadEvolutionStream() {
  monitorStore.setLoading('evolution', true)
  try {
    const data = await getEvolutionStream(50, 0)
    monitorStore.setEvolutionEvents(data.events, data.total)
  } finally {
    monitorStore.setLoading('evolution', false)
  }
}

/**
 * 加载诊断结果
 */
async function loadDiagnosis() {
  monitorStore.setLoading('diagnosis', true)
  try {
    const data = await getDiagnosis()
    monitorStore.setDiagnosis(data)
  } finally {
    monitorStore.setLoading('diagnosis', false)
  }
}

/**
 * 加载 Agent 性能
 */
async function loadAgentPerformance() {
  monitorStore.setLoading('agents', true)
  try {
    const agents = await getAgentPerformance('all')
    monitorStore.setAgentPerformance(agents)
  } finally {
    monitorStore.setLoading('agents', false)
  }
}

/**
 * 加载知识图谱
 */
async function loadKnowledgeGraph() {
  monitorStore.setLoading('knowledge', true)
  try {
    const data = await getKnowledgeGraph('all', '')
    monitorStore.setKnowledgeGraph(data)
  } finally {
    monitorStore.setLoading('knowledge', false)
  }
}

/**
 * 建立 WebSocket 连接
 */
function connectWebSocket() {
  const token = userStore.token || 'guest'

  ws.value = createWebSocket(
    token,
    (event) => {
      // 接收到新的进化事件
      monitorStore.addEvolutionEvent(event)
      monitorStore.setWsConnected(true)
    },
    (error) => {
      console.error('[Monitor] WebSocket 错误:', error)
      monitorStore.setWsConnected(false)
    }
  )
}

/**
 * 刷新所有数据
 */
async function handleRefresh() {
  refreshing.value = true
  await loadAllData()
  refreshing.value = false
}
</script>

<template>
  <div class="monitor-page">
    <!-- Header -->
    <div class="monitor-header">
      <h1 class="monitor-title">
        <span class="icon">🤖</span>
        Claude Dev Team 监控中心
      </h1>
      <div class="monitor-actions">
        <span v-if="monitorStore.wsConnected" class="ws-status connected">
          🟢 实时连接
        </span>
        <span v-else class="ws-status disconnected">
          🔴 连接断开
        </span>
        <button
          class="refresh-btn"
          :disabled="refreshing"
          @click="handleRefresh"
        >
          {{ refreshing ? '刷新中...' : '🔄 刷新数据' }}
        </button>
      </div>
    </div>

    <!-- 智能诊断中心（置顶） -->
    <MonitorDiagnosis />

    <!-- 智能水平走势图 -->
    <MonitorIntelligenceChart />

    <!-- 两列布局 -->
    <div class="monitor-grid">
      <!-- 左侧：实时进化动态 -->
      <div class="monitor-col">
        <MonitorEvolutionStream />
      </div>

      <!-- 右侧：Agent 性能监控 -->
      <div class="monitor-col">
        <MonitorAgentProgress />
      </div>
    </div>

    <!-- 知识图谱 -->
    <MonitorKnowledgeGraph />
  </div>
</template>

<style scoped>
.monitor-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.monitor-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.monitor-title .icon {
  font-size: 32px;
}

.monitor-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.ws-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.ws-status.connected {
  background: #d4edda;
  color: #155724;
}

.ws-status.disconnected {
  background: #f8d7da;
  color: #721c24;
}

.refresh-btn {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.monitor-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.monitor-col {
  min-height: 400px;
}

@media (max-width: 1024px) {
  .monitor-grid {
    grid-template-columns: 1fr;
  }
}
</style>
