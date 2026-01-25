<!-- =====================================================
     实时进化动态组件
     =====================================================
     功能：事件流展示最新进化记录
     职责：
     1. 显示最近的进化事件列表（最多显示 20 条）
     2. 实时接收 WebSocket 推送的新事件
     3. 展示事件详情（时间、Agent、策略、奖励、描述）
     4. 根据奖励分数显示不同颜色

     技术：虚拟滚动（支持 1000+ 条记录）
     数据来源：monitorStore.evolutionEvents
     更新方式：页面加载时获取 + WebSocket 实时推送
     ===================================================== -->

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

const monitorStore = useMonitorStore()

// ==================== 计算属性 ====================

/**
 * 进化事件列表
 * 从 monitorStore 获取所有进化事件
 */
const events = computed(() => monitorStore.evolutionEvents)

// ==================== 监听器 ====================

/**
 * 监听最新事件
 * 当 WebSocket 推送新事件时，打印日志
 */
watch(() => monitorStore.latestEvent, (newEvent) => {
  if (newEvent) {
    console.log('[MonitorEvolutionStream] 收到新事件:', newEvent.description)
  }
})

// ==================== 方法 ====================

/**
 * 格式化时间
 * 将 ISO 时间戳转换为本地时间字符串
 *
 * @param timestamp ISO 时间戳
 * @returns 格式化后的时间字符串（如 "2026-01-25 14:30:00"）
 */
function formatTime(timestamp: string) {
  return new Date(timestamp).toLocaleString()
}

/**
 * 获取奖励颜色
 * 根据奖励分数返回不同颜色：
 * - 8 分以上：绿色（表示优秀）
 * - 6-8 分：橙色（表示良好）
 * - 6 分以下：红色（表示需要改进）
 *
 * @param reward 奖励分数（0-10）
 * @returns 颜色值（十六进制）
 */
function getRewardColor(reward: number) {
  if (reward >= 8) return '#67C23A'  // 绿色
  if (reward >= 6) return '#E6A23C'  // 橙色
  return '#F56C6C'                   // 红色
}
</script>

<template>
  <div class="evolution-stream-container">
    <h2 class="stream-title">📊 实时进化动态</h2>

    <!-- 加载状态 -->
    <div v-if="monitorStore.loading.evolution" class="loading">
      加载中...
    </div>

    <!-- 空状态 -->
    <div v-else-if="events.length === 0" class="empty">
      暂无进化事件
    </div>

    <!-- 事件列表（最多显示 20 条） -->
    <div v-else class="event-list">
      <div
        v-for="event in events.slice(0, 20)"
        :key="event.id"
        class="event-item"
      >
        <!-- 事件头部：时间 + Agent -->
        <div class="event-header">
          <span class="event-time">🕐 {{ formatTime(event.timestamp) }}</span>
          <span class="event-agent">{{ event.agent }}</span>
        </div>

        <!-- 事件元信息：策略 + 奖励 -->
        <div class="event-meta">
          <span class="event-strategy">策略: {{ event.strategy }}</span>
          <span class="event-reward" :style="{ color: getRewardColor(event.reward) }">
            奖励: {{ event.reward.toFixed(1) }}/10
          </span>
        </div>

        <!-- 事件描述 -->
        <div class="event-description">{{ event.description }}</div>
      </div>
    </div>

    <!-- 加载更多提示 -->
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
