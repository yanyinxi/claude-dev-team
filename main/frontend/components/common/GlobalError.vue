<script setup lang="ts">
import { ref } from 'vue'
import { useNetworkStatus } from '@/composables/useNetworkStatus'

// =====================================================
// 全局错误提示组件
// 功能：显示网络错误、API 错误等
// =====================================================

interface ErrorInfo {
  id: number
  type: 'error' | 'warning' | 'success'
  message: string
  duration?: number
}

const errors = ref<ErrorInfo[]>([])
let errorId = 0

const { showOfflineWarning } = useNetworkStatus()

// =====================================================
// 错误处理函数
// =====================================================

/**
 * 显示全局错误提示
 * 必要注释：用于显示 API 错误、网络错误等
 */
function showError(message: string, duration = 5000) {
  const id = ++errorId
  errors.value.push({
    id,
    type: 'error',
    message,
    duration
  })

  // 自动移除
  if (duration > 0) {
    setTimeout(() => {
      removeError(id)
    }, duration)
  }

  return id
}

/**
 * 显示全局成功提示
 */
function showSuccess(message: string, duration = 3000) {
  const id = ++errorId
  errors.value.push({
    id,
    type: 'success',
    message,
    duration
  })

  if (duration > 0) {
    setTimeout(() => {
      removeError(id)
    }, duration)
  }
}

/**
 * 移除错误提示
 */
function removeError(id: number) {
  const index = errors.value.findIndex(e => e.id === id)
  if (index > -1) {
    errors.value.splice(index, 1)
  }
}

// =====================================================
// 导出方法和状态
// =====================================================

defineExpose({
  showError,
  showSuccess,
  removeError
})
</script>

<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <!-- 离线警告 -->
    <Transition name="slide">
      <div
        v-if="showOfflineWarning"
        class="bg-yellow-500 text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3"
      >
        <span class="text-2xl">📡</span>
        <div>
          <p class="font-bold">网络连接已断开</p>
          <p class="text-sm opacity-90">请检查您的网络设置</p>
        </div>
      </div>
    </Transition>

    <!-- 错误/成功提示 -->
    <TransitionGroup name="slide">
      <div
        v-for="error in errors"
        :key="error.id"
        :class="[
          'px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 min-w-[300px]',
          error.type === 'error' ? 'bg-red-500' : '',
          error.type === 'warning' ? 'bg-yellow-500' : '',
          error.type === 'success' ? 'bg-green-500' : ''
        ]"
      >
        <span class="text-2xl">
          {{ error.type === 'error' ? '❌' : error.type === 'success' ? '✅' : '⚠️' }}
        </span>
        <p class="font-medium text-white flex-1">{{ error.message }}</p>
        <button
          @click="removeError(error.id)"
          class="text-white/80 hover:text-white transition"
        >
          ✕
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.slide-move {
  transition: transform 0.3s ease;
}
</style>
