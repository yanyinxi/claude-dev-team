// =====================================================
// 网络状态检测 Composable
// 功能：检测网络连接状态，提供在线/离线事件监听
// =====================================================

import { ref, onMounted, onUnmounted } from 'vue'

// =====================================================
// 全局网络状态
// =====================================================

const isOnline = ref(true)
const showOfflineWarning = ref(false)

// =====================================================
// 网络状态 Composable
// =====================================================

export function useNetworkStatus() {
  // =====================================================
  // 事件处理函数
  // =====================================================

  /**
   * 网络恢复连接时的处理
   * 重要注释：隐藏离线警告，刷新页面数据
   */
  function handleOnline() {
    isOnline.value = true
    showOfflineWarning.value = false
    console.log('✅ 网络已恢复')
    // 可以在这里触发数据刷新
  }

  /**
   * 网络断开时的处理
   * 重要注释：显示离线警告，保存未提交数据
   */
  function handleOffline() {
    isOnline.value = false
    showOfflineWarning.value = true
    console.warn('⚠️ 网络已断开')
  }

  // =====================================================
  // 生命周期
  // =====================================================

  onMounted(() => {
    // 初始化网络状态
    isOnline.value = navigator.onLine

    // 监听网络状态变化
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
  })

  onUnmounted(() => {
    // 移除事件监听
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
  })

  // =====================================================
  // 返回状态和方法
  // =====================================================

  return {
    isOnline,
    showOfflineWarning,
    // 手动关闭警告
    dismissWarning: () => {
      showOfflineWarning.value = false
    }
  }
}

// =====================================================
// 网络请求封装 - 带自动重试
// =====================================================

export async function fetchWithRetry(
  fetchFn: () => Promise<any>,
  options: {
    maxRetries?: number
    retryDelay?: number
    onRetry?: (attempt: number, error: any) => void
  } = {}
): Promise<any> {
  const { maxRetries = 2, retryDelay = 1000, onRetry } = options
  let lastError: any

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fetchFn()
    } catch (error: any) {
      lastError = error

      // 如果是不可重试的错误，直接抛出
      if (!error.isRetryable) {
        throw error
      }

      // 如果还有重试次数，等待后重试
      if (attempt < maxRetries) {
        console.warn(`请求失败，第 ${attempt + 1} 次重试...`)
        onRetry?.(attempt + 1, error)
        await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)))
      }
    }
  }

  throw lastError
}
