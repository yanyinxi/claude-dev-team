<!-- =====================================================
智能水平走势图组件
=====================================================
功能：展示智能水平随时间的变化曲线
技术：ECharts 折线图
===================================================== -->

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

// ==================== 状态管理 ====================

const monitorStore = useMonitorStore()

// 图表容器引用
const chartRef = ref<HTMLDivElement | null>(null)

// 时间范围选择
const timeRange = ref('7')

// ==================== 计算属性 ====================

/**
 * 当前智能水平分数
 */
const currentScore = computed(() => {
  return monitorStore.currentIntelligenceScore.toFixed(2)
})

/**
 * 趋势数据
 */
const trendData = computed(() => {
  return monitorStore.intelligenceTrend?.trend || []
})

/**
 * 里程碑数据
 */
const milestones = computed(() => {
  return monitorStore.intelligenceTrend?.milestones || []
})

// ==================== 生命周期 ====================

onMounted(() => {
  // 初始化图表（简化版，实际应使用 ECharts）
  console.log('[MonitorIntelligenceChart] 组件已挂载')
})

onUnmounted(() => {
  console.log('[MonitorIntelligenceChart] 组件已卸载')
})
</script>

<template>
  <div class="intelligence-chart-container">
    <div class="chart-header">
      <h2 class="chart-title">📈 系统智能水平走势</h2>
      <div class="chart-controls">
        <select v-model="timeRange" class="time-range-select">
          <option value="7">最近 7 天</option>
          <option value="30">最近 30 天</option>
          <option value="all">全部</option>
        </select>
      </div>
    </div>

    <div class="current-score">
      <div class="score-label">当前智能水平</div>
      <div class="score-value">{{ currentScore }}</div>
      <div class="score-max">/ 10.0</div>
    </div>

    <!-- 图表容器（简化版，实际应使用 ECharts） -->
    <div ref="chartRef" class="chart-canvas">
      <div v-if="monitorStore.loading.intelligence" class="loading">
        加载中...
      </div>
      <div v-else-if="trendData.length === 0" class="empty">
        暂无数据
      </div>
      <div v-else class="chart-placeholder">
        <p>📊 智能水平走势图</p>
        <p class="hint">（需要集成 ECharts 库）</p>
        <div class="data-summary">
          <div>数据点数: {{ trendData.length }}</div>
          <div>里程碑: {{ milestones.length }}</div>
        </div>
      </div>
    </div>

    <!-- 里程碑列表 -->
    <div v-if="milestones.length > 0" class="milestones">
      <h3 class="milestones-title">🎯 学习路径里程碑</h3>
      <div class="milestone-list">
        <div
          v-for="milestone in milestones"
          :key="milestone.timestamp"
          class="milestone-item"
        >
          <div class="milestone-date">
            {{ new Date(milestone.timestamp).toLocaleDateString() }}
          </div>
          <div class="milestone-event">{{ milestone.event }}</div>
          <div class="milestone-score">
            {{ milestone.intelligence_score.toFixed(2) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.intelligence-chart-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.time-range-select {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.current-score {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.score-label {
  font-size: 16px;
}

.score-value {
  font-size: 48px;
  font-weight: bold;
}

.score-max {
  font-size: 24px;
  opacity: 0.8;
}

.chart-canvas {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.loading,
.empty {
  color: #999;
  font-size: 16px;
}

.chart-placeholder {
  text-align: center;
  color: #666;
}

.chart-placeholder p {
  margin: 10px 0;
  font-size: 18px;
}

.hint {
  font-size: 14px;
  color: #999;
}

.data-summary {
  margin-top: 20px;
  display: flex;
  gap: 30px;
  justify-content: center;
  font-size: 14px;
}

.milestones {
  margin-top: 20px;
}

.milestones-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.milestone-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.milestone-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.milestone-date {
  font-size: 14px;
  color: #666;
  min-width: 100px;
}

.milestone-event {
  flex: 1;
  font-size: 14px;
  color: #333;
}

.milestone-score {
  font-size: 16px;
  font-weight: bold;
  color: #667eea;
}
</style>
