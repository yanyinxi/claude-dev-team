<!-- =====================================================
Agent 性能监控组件
=====================================================
功能：展示所有 Agent 的当前进度和历史性能数据
===================================================== -->

<script setup lang="ts">
import { computed } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

const monitorStore = useMonitorStore()

// Agent 列表
const agents = computed(() => monitorStore.agentPerformance)

// 获取进度条颜色
function getProgressColor(progress: number) {
  if (progress >= 80) return '#67C23A'
  if (progress >= 50) return '#E6A23C'
  return '#F56C6C'
}

// 获取状态徽章
function getStatusBadge(status: string) {
  const badges = {
    working: { text: '工作中', color: '#67C23A' },
    completed: { text: '已完成', color: '#409EFF' },
    failed: { text: '失败', color: '#F56C6C' },
    idle: { text: '空闲', color: '#909399' }
  }
  return badges[status as keyof typeof badges] || badges.idle
}

// 格式化时长
function formatDuration(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}
</script>

<template>
  <div class="agent-progress-container">
    <h2 class="progress-title">🤖 Agent 性能监控</h2>

    <div v-if="monitorStore.loading.agents" class="loading">
      加载中...
    </div>

    <div v-else-if="agents.length === 0" class="empty">
      暂无 Agent 数据
    </div>

    <div v-else class="agent-list">
      <div
        v-for="agent in agents"
        :key="agent.name"
        class="agent-item"
      >
        <div class="agent-header">
          <span class="agent-name">{{ agent.name }}</span>
          <span
            class="agent-status"
            :style="{ background: getStatusBadge(agent.status).color }"
          >
            {{ getStatusBadge(agent.status).text }}
          </span>
        </div>

        <div class="progress-bar-container">
          <div
            class="progress-bar"
            :style="{
              width: agent.current_progress + '%',
              background: getProgressColor(agent.current_progress)
            }"
          ></div>
        </div>

        <div class="agent-stats">
          <span>总任务: {{ agent.performance.total_tasks }}</span>
          <span>成功率: {{ (agent.performance.success_rate * 100).toFixed(0) }}%</span>
          <span>平均耗时: {{ formatDuration(agent.performance.avg_duration_seconds) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.agent-progress-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.progress-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.loading,
.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.agent-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.agent-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.agent-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.agent-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
}

.progress-bar-container {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-bar {
  height: 100%;
  transition: width 0.3s;
}

.agent-stats {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
}
</style>
