<!-- =====================================================
监控系统主页面
=====================================================
功能：监控中心主页面，包含 5 个子组件
职责：
1. 布局管理：组织 5 个监控子组件的布局
2. WebSocket 连接管理：建立和维护实时数据推送连接
3. 全局状态初始化：页面加载时获取所有监控数据
4. 数据刷新：提供手动刷新所有数据的功能

子组件：
- MonitorIntelligenceChart：智能水平走势图
- MonitorDiagnosis：智能诊断中心
- MonitorEvolutionStream：实时进化动态
- MonitorAgentProgress：Agent 性能监控
- MonitorKnowledgeGraph：知识图谱

数据流：
1. 页面加载 → 并行获取所有数据 → 存入 monitorStore
2. WebSocket 连接 → 实时推送进化事件 → 更新 monitorStore
3. 手动刷新 → 重新获取所有数据 → 更新 monitorStore
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

// ==================== 响应式数据 ====================

/**
 * WebSocket 连接实例
 * 用于接收实时进化事件推送
 */
const ws = ref<WebSocket | null>(null)

/**
 * 刷新状态
 * 控制刷新按钮的禁用状态和文本显示
 */
const refreshing = ref(false)

/**
 * 功能说明展开状态
 * 控制功能说明卡片的展开/收起
 */
const showDescription = ref(true)

// ==================== 生命周期钩子 ====================

/**
 * 组件挂载时
 * 1. 并行加载所有监控数据
 * 2. 建立 WebSocket 连接接收实时推送
 */
onMounted(async () => {
  // 初始化数据
  await loadAllData()

  // 建立 WebSocket 连接
  connectWebSocket()
})

/**
 * 组件卸载时
 * 断开 WebSocket 连接，释放资源
 */
onUnmounted(() => {
  // 断开 WebSocket 连接
  if (ws.value) {
    ws.value.close()
  }
})

// ==================== 方法 ====================

/**
 * 加载所有数据
 * 并行加载 5 个监控模块的数据，提高加载效率
 *
 * 加载顺序（并行）：
 * 1. 智能水平走势（最近 7 天）
 * 2. 进化事件流（最近 50 条）
 * 3. 智能诊断结果
 * 4. Agent 性能数据
 * 5. 知识图谱数据
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
 * 获取最近 7 天的智能水平数据和里程碑事件
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
 * 获取最近 50 条进化事件记录
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
 * 获取最新的智能诊断结果和问题列表
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
 * 获取所有 Agent 的性能数据和工作状态
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
 * 获取所有类型的知识条目
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
 * 连接到后端 WebSocket 服务，接收实时进化事件推送
 *
 * 功能：
 * 1. 使用用户 Token 进行身份验证
 * 2. 接收新的进化事件并更新 store
 * 3. 维护连接状态（心跳保活）
 * 4. 处理连接错误和断开
 */
function connectWebSocket() {
  const token = userStore.token || 'guest'

  ws.value = createWebSocket(
    token,
    (event) => {
      // 接收到新的进化事件
      monitorStore.addEvolutionEvent(event)
    },
    () => {
      // WebSocket 连接成功
      monitorStore.setWsConnected(true)
    },
    (error) => {
      // WebSocket 错误
      console.error('[Monitor] WebSocket 错误:', error)
      monitorStore.setWsConnected(false)
    },
    () => {
      // WebSocket 连接关闭
      monitorStore.setWsConnected(false)
    }
  )
}

/**
 * 刷新所有数据
 * 手动触发重新加载所有监控数据
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

    <!-- 功能说明卡片 -->
    <div class="description-card">
      <div class="description-header" @click="showDescription = !showDescription">
        <h2 class="description-title">📊 监控中心功能说明</h2>
        <button class="toggle-btn">
          {{ showDescription ? '▼ 收起' : '▶ 展开' }}
        </button>
      </div>
      <div v-show="showDescription" class="description-content">
        <div class="description-section">
          <h3 class="section-title">🤖 智能水平走势</h3>
          <ul class="section-list">
            <li>实时监控系统的智能水平（0-10分）</li>
            <li>追踪策略权重、知识丰富度、质量趋势等指标</li>
            <li>显示最近7天/30天的进化趋势</li>
          </ul>
        </div>

        <div class="description-section">
          <h3 class="section-title">🔍 智能诊断中心</h3>
          <ul class="section-list">
            <li>自动扫描代码库，发现性能、安全、质量问题</li>
            <li>提供修复建议和自动修复代码</li>
            <li>支持一键修复部分问题</li>
          </ul>
        </div>

        <div class="description-section">
          <h3 class="section-title">🤖 Agent 性能监控</h3>
          <ul class="section-list">
            <li>监控11个AI代理的工作状态和性能</li>
            <li>显示任务统计、执行时间、成功率</li>
            <li>追踪实时进度和最后活跃时间</li>
          </ul>
        </div>

        <div class="description-section">
          <h3 class="section-title">📚 知识图谱</h3>
          <ul class="section-list">
            <li>展示系统积累的策略、最佳实践、模板</li>
            <li>支持按类型筛选和关键词搜索</li>
          </ul>
        </div>
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

.description-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.description-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.description-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.toggle-btn {
  padding: 6px 12px;
  background: #f0f0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s;
}

.toggle-btn:hover {
  background: #e0e0e0;
}

.description-content {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.description-section {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.section-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.section-list li {
  padding: 6px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.section-list li::before {
  content: '• ';
  color: #667eea;
  font-weight: bold;
  margin-right: 8px;
}

@media (max-width: 768px) {
  .description-content {
    grid-template-columns: 1fr;
  }
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
