import { ref } from 'vue'

// =====================================================
// 浏览器通知 + Web Audio 提示音 Composable
// 功能：
//   1. 请求/检查 Notification API 权限
//   2. 发送桌面通知
//   3. 用 Web Audio API 生成 440Hz beep（无需外部音频文件）
// 优雅降级：权限被拒绝时不抛错，只影响桌面通知部分
// =====================================================

/** Notification 权限状态 */
export type NotificationPermission = 'default' | 'granted' | 'denied' | 'unsupported'

export function useNotification() {
  // 当前通知权限状态
  const hasPermission = ref<NotificationPermission>(
    typeof Notification !== 'undefined' ? Notification.permission : 'unsupported'
  )

  /**
   * 请求浏览器通知权限
   * 返回最终权限状态
   */
  async function requestPermission(): Promise<NotificationPermission> {
    if (typeof Notification === 'undefined') {
      hasPermission.value = 'unsupported'
      return 'unsupported'
    }

    if (Notification.permission === 'granted') {
      hasPermission.value = 'granted'
      return 'granted'
    }

    // 调用浏览器权限弹窗
    const result = await Notification.requestPermission()
    hasPermission.value = result as NotificationPermission
    return result as NotificationPermission
  }

  /**
   * 发送桌面通知
   * 如果权限未授予则静默失败（不抛错）
   */
  function notify(title: string, body: string, options?: NotificationOptions): void {
    if (typeof Notification === 'undefined') return
    if (Notification.permission !== 'granted') return

    try {
      new Notification(title, {
        body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        requireInteraction: false,
        ...options
      })
    } catch (e) {
      // Service Worker 环境或隐私模式下可能报错，静默处理
      console.warn('[useNotification] 发送通知失败:', e)
    }
  }

  /**
   * 用 Web Audio API 生成 440Hz beep 提示音
   * 时长约 300ms，无需任何外部音频资源
   */
  function playBeep(): void {
    try {
      // 每次调用创建独立的 AudioContext，避免状态残留
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
      if (!AudioCtx) {
        console.warn('[useNotification] 当前浏览器不支持 Web Audio API')
        return
      }

      const ctx = new AudioCtx()

      // 主 oscillator：440Hz 正弦波
      const oscillator = ctx.createOscillator()
      oscillator.type = 'sine'
      oscillator.frequency.setValueAtTime(440, ctx.currentTime)

      // GainNode 控制音量包络，避免爆音
      const gainNode = ctx.createGain()
      gainNode.gain.setValueAtTime(0, ctx.currentTime)
      gainNode.gain.linearRampToValueAtTime(0.6, ctx.currentTime + 0.01)   // 快速淡入
      gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3) // 淡出到静音

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      oscillator.start(ctx.currentTime)
      oscillator.stop(ctx.currentTime + 0.3)

      // 播放完毕后释放 AudioContext
      oscillator.onended = () => {
        ctx.close().catch(() => { /* ignore */ })
      }
    } catch (e) {
      console.warn('[useNotification] 播放 beep 失败:', e)
    }
  }

  /**
   * 一次性触发所有通知形式：beep + 桌面通知
   * 页面内弹窗由调用方自行控制
   */
  function triggerAll(title: string, body: string): void {
    playBeep()
    notify(title, body)
  }

  return {
    hasPermission,
    requestPermission,
    notify,
    playBeep,
    triggerAll
  }
}
