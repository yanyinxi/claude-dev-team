<!-- =====================================================
智能水平走势图组件
=====================================================
功能：展示智能水平随时间的变化曲线
技术：ECharts 折线图
===================================================== -->

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'

// ==================== 状态管理 ====================

const monitorStore = useMonitorStore()

// 图表容器引用
const chartRef = ref<HTMLDivElement | null>(null)

// ECharts 实例
let chartInstance: ECharts | null = null

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

// ==================== 方法 ====================

/**
 * 初始化 ECharts 图表
 */
function initChart() {
  // 使用 nextTick 确保 DOM 已经渲染
  nextTick(() => {
    if (!chartRef.value) {
      console.warn('[ECharts] 图表容器未找到')
      return
    }

    try {
      // 创建 ECharts 实例
      chartInstance = echarts.init(chartRef.value)

      // 更新图表数据
      updateChart()

      // 监听窗口大小变化
      window.addEventListener('resize', handleResize)
    } catch (error) {
      console.error('[ECharts] 初始化失败:', error)
    }
  })
}

/**
 * 更新图表数据
 */
function updateChart() {
  if (!chartInstance) {
    console.warn('[ECharts] 图表实例不存在')
    return
  }

  if (!trendData.value || trendData.value.length === 0) {
    console.warn('[ECharts] 暂无数据')
    return
  }

  try {
    // 准备数据
    const dates = trendData.value.map((item) => {
      const date = new Date(item.timestamp)
      return `${date.getMonth() + 1}/${date.getDate()}`
    })

    const scores = trendData.value.map((item) => item.intelligence_score)

    // 准备里程碑标记数据
    const milestoneMarks = milestones.value.map((milestone) => {
      const date = new Date(milestone.timestamp)
      return {
        name: milestone.event,
        xAxis: `${date.getMonth() + 1}/${date.getDate()}`,
        yAxis: milestone.intelligence_score,
        value: milestone.intelligence_score.toFixed(2)
      }
    })

    // 配置图表选项
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const data = params[0]
          return `${data.axisValue}<br/>智能水平: ${data.value.toFixed(2)}`
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: false,
        axisLine: {
          lineStyle: {
            color: '#999'
          }
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 10,
        axisLine: {
          lineStyle: {
            color: '#999'
          }
        },
        splitLine: {
          lineStyle: {
            color: '#eee'
          }
        }
      },
      series: [
        {
          name: '智能水平',
          type: 'line',
          smooth: true,
          data: scores,
          lineStyle: {
            color: '#667eea',
            width: 3
          },
          itemStyle: {
            color: '#667eea'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
                { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
              ]
            }
          },
          markPoint: {
            data: milestoneMarks.map((mark) => ({
              name: mark.name,
              coord: [mark.xAxis, mark.yAxis],
              value: mark.value,
              symbol: 'pin',
              symbolSize: 50,
              itemStyle: {
                color: '#ff6b6b'
              },
              label: {
                show: true,
                formatter: '{b}',
                fontSize: 10
              }
            }))
          }
        }
      ]
    }

    // 设置图表选项
    chartInstance.setOption(option)
  } catch (error) {
    console.error('[ECharts] 更新图表失败:', error)
  }
}

/**
 * 处理窗口大小变化
 */
function handleResize() {
  if (chartInstance) {
    chartInstance.resize()
  }
}

/**
 * 销毁图表
 */
function destroyChart() {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
}

// ==================== 生命周期 ====================

onMounted(() => {
  // 初始化图表
  initChart()
})

onUnmounted(() => {
  // 销毁图表
  destroyChart()
})

// ==================== 监听数据变化 ====================

watch(trendData, () => {
  // 数据变化时更新图表
  updateChart()
})

watch(timeRange, async (newRange) => {
  // 时间范围变化时重新加载数据
  monitorStore.setLoading('intelligence', true)
  try {
    const { getIntelligenceTrend } = await import('@/services/monitor')
    const data = await getIntelligenceTrend(newRange)
    monitorStore.setIntelligenceTrend(data)
  } finally {
    monitorStore.setLoading('intelligence', false)
  }
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

    <!-- 图表容器 -->
    <div ref="chartRef" class="chart-canvas">
      <div v-if="monitorStore.loading.intelligence" class="loading">
        加载中...
      </div>
      <div v-else-if="trendData.length === 0" class="empty">
        暂无数据
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
  height: 400px;
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
