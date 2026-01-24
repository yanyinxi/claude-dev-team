<script setup lang="ts">
import { computed } from 'vue'
import { useAlarmStore } from '@/stores/alarmStore'

// =====================================================
// 学习倒计时组件
// 功能：显示学习/休息倒计时，最后 5 分钟警告
// =====================================================

const alarmStore = useAlarmStore()

// 倒计时颜色（根据状态变化）
const timerColor = computed(() => {
  if (alarmStore.isWarning) {
    return 'text-red-500'  // 最后 5 分钟警告
  }
  if (alarmStore.isStudying) {
    return 'text-blue-500'  // 学习中
  }
  if (alarmStore.isResting) {
    return 'text-orange-500'  // 休息中
  }
  return 'text-gray-400'  // 空闲
})

// 状态文本
const statusText = computed(() => {
  if (alarmStore.isStudying) {
    return '学习中'
  }
  if (alarmStore.isResting) {
    return '休息中'
  }
  return '未开始'
})

// 状态图标
const statusIcon = computed(() => {
  if (alarmStore.isStudying) {
    return '📚'
  }
  if (alarmStore.isResting) {
    return '☕'
  }
  return '⏸️'
})
</script>

<template>
  <div class="alarm-countdown">
    <!-- 倒计时显示 -->
    <div class="flex items-center gap-3 bg-white rounded-2xl shadow-lg px-6 py-4">
      <!-- 状态图标 -->
      <div class="text-3xl">{{ statusIcon }}</div>

      <!-- 倒计时时间 -->
      <div class="flex flex-col">
        <div class="text-sm text-gray-500">{{ statusText }}</div>
        <div :class="['text-3xl font-bold font-mono', timerColor]">
          {{ alarmStore.remainingTime }}
        </div>
      </div>

      <!-- 警告提示 -->
      <div v-if="alarmStore.isWarning" class="ml-auto">
        <div class="flex items-center gap-2 bg-red-50 text-red-600 px-3 py-2 rounded-lg animate-pulse">
          <span class="text-xl">⚠️</span>
          <span class="text-sm font-medium">快结束了！</span>
        </div>
      </div>
    </div>

    <!-- 进度条 -->
    <div v-if="!alarmStore.isIdle" class="mt-3 bg-gray-200 rounded-full h-2 overflow-hidden">
      <div
        class="h-full transition-all duration-1000 ease-linear"
        :class="{
          'bg-blue-500': alarmStore.isStudying && !alarmStore.isWarning,
          'bg-red-500': alarmStore.isWarning,
          'bg-orange-500': alarmStore.isResting
        }"
        :style="{ width: `${alarmStore.progressPercent}%` }"
      ></div>
    </div>

    <!-- 规则信息 -->
    <div v-if="alarmStore.status.rule" class="mt-2 text-xs text-gray-500 text-center">
      学习 {{ alarmStore.status.rule.study_duration }} 分钟 / 休息 {{ alarmStore.status.rule.rest_duration }} 分钟
    </div>
  </div>
</template>

<style scoped>
.alarm-countdown {
  @apply w-full max-w-md mx-auto;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
