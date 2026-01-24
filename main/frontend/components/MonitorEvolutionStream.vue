<!-- =====================================================
实时进化动态组件
=====================================================
功能：事件流展示最新进化记录
技术：虚拟滚动（支持 1000+ 条记录）
===================================================== -->

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

const monitorStore = useMonitorStore()

// 进化事件列表
const events = computed(() => monitorStore.evolutionEvents)

// 监听最新事件
watch(() => monitorStore.latestEvent, (newEvent) => {
  if (newEvent) {
    console.log('[MonitorEvolutionStream] 收到新事件:', newEvent.description)
  }
})

// 格式化时间
function formatTime(timestamp: string) {
  return new Date(timestamp).toLocaleString()
}

// 获取奖励颜色
function getRewardColor(reward: number) {
  if (reward >= 8) return '#67C23A'
  if (reward >= 6) return '#E6A23C'
  return '#F56C6C'
}
</script>

<template>
  <div class="evolution-stream-container">
    <h2 class="stream-title">📊 实时进化动态</h2>

    <div v-if="monitorStore.loading.evolution" class="loading">
      加载中...
    </div>

    <div v-else-if="events.length === 0" class="empty">
      暂无进化事件
    </div>

    <div v-else class="event-list">
      <div
        v-for="event in events.slice(0, 20)"
        :key="event.id"
        class="event-item"
      >
        <div class="event-header">
          <span class="event-time">🕐 {{ formatTime(event.timestamp) }}</span>
          <span class="event-agent">{{ event.agent }}</span>
        </div>
        <div class="event-meta">
          <span class="event-strategy">策略: {{ event.strategy }}</span>
          <span class="event-reward" :style="{ color: getRewardColor(event.reward) }">
            奖励: {{ event.reward.toFixed(1) }}/10
          </span>
        </div>
        <div class="event-description">{{ event.description }}</div>
      </div>
    </div>

    <div v-if="events.length > 20" class="load-more">
      显示 20 / {{ events.length }} 条记录
    </div>
  </div>
</template>

<style scoped>
.evolution-stream-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.stream-title {
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

.event-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.event-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s;
}

.event-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-time {
  font-size: 13px;
  color: #666;
}

.event-agent {
  padding: 4px 12px;
  background: white;
  border-radius: 12px;
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
}

.event-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 13px;
}

.event-strategy {
  color: #888;
}

.event-reward {
  font-weight: bold;
}

.event-description {
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

.load-more {
  text-align: center;
  padding: 15px;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #eee;
  margin-top: 15px;
}
</style>
