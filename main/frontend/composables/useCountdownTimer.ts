import { ref, computed, onUnmounted } from 'vue'

// =====================================================
// 通用倒计时 Composable
// 功能：独立倒计时逻辑，不依赖后端
// 精度：使用 Date.now() 避免 tab 切换后的计时误差
// =====================================================

export type TimerState = 'idle' | 'running' | 'paused'

export interface CountdownTimerOptions {
  /** 倒计时结束时的回调 */
  onComplete?: () => void
}

export function useCountdownTimer(options: CountdownTimerOptions = {}) {
  // 总时长（秒），用户设定
  const duration = ref<number>(0)
  // 剩余秒数
  const remaining = ref<number>(0)
  // 当前状态
  const state = ref<TimerState>('idle')

  // 内部计时器变量
  let intervalId: ReturnType<typeof setInterval> | null = null
  // 记录本段运行开始时的时间戳，用于 Date.now() 精度校正
  let segmentStartTime: number = 0
  // 记录本段运行开始时剩余的秒数
  let segmentStartRemaining: number = 0

  // ---- computed ----

  /** 是否正在运行 */
  const isRunning = computed(() => state.value === 'running')

  /** 是否已暂停 */
  const isPaused = computed(() => state.value === 'paused')

  /**
   * 进度 0-100，表示已经消耗的百分比
   * 0 = 刚开始，100 = 全部耗尽
   */
  const progress = computed(() => {
    if (duration.value <= 0) return 0
    const consumed = duration.value - remaining.value
    return Math.min(100, Math.max(0, (consumed / duration.value) * 100))
  })

  /** "MM:SS" 格式的剩余时间 */
  const formattedTime = computed(() => {
    const total = Math.max(0, remaining.value)
    const m = Math.floor(total / 60)
    const s = total % 60
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  })

  // ---- 内部方法 ----

  /** 清除 interval */
  function clearTimer() {
    if (intervalId !== null) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  /** 启动内部 tick，基于 Date.now() 校准剩余时间 */
  function startTick() {
    segmentStartTime = Date.now()
    segmentStartRemaining = remaining.value

    intervalId = setInterval(() => {
      const elapsed = Math.floor((Date.now() - segmentStartTime) / 1000)
      const newRemaining = segmentStartRemaining - elapsed

      if (newRemaining <= 0) {
        remaining.value = 0
        clearTimer()
        state.value = 'idle'
        options.onComplete?.()
      } else {
        remaining.value = newRemaining
      }
    }, 200) // 200ms 轮询，保证 UI 秒级更新且精度足够
  }

  // ---- 公开方法 ----

  /**
   * 开始倒计时
   * @param seconds 可选：重新设置总时长（秒）
   */
  function start(seconds?: number) {
    clearTimer()
    if (seconds !== undefined && seconds > 0) {
      duration.value = seconds
      remaining.value = seconds
    } else if (state.value === 'idle') {
      // 已在 idle 但没传 seconds：从 duration 重新开始
      remaining.value = duration.value
    }
    if (duration.value <= 0) return
    state.value = 'running'
    startTick()
  }

  /** 暂停倒计时 */
  function pause() {
    if (state.value !== 'running') return
    clearTimer()
    state.value = 'paused'
  }

  /** 从暂停处恢复 */
  function resume() {
    if (state.value !== 'paused') return
    state.value = 'running'
    startTick()
  }

  /**
   * 重置：停止计时，剩余时间恢复为总时长，状态回到 idle
   */
  function reset() {
    clearTimer()
    remaining.value = duration.value
    state.value = 'idle'
  }

  // 组件卸载时清理定时器，防止内存泄漏
  onUnmounted(() => {
    clearTimer()
  })

  return {
    duration,
    remaining,
    isRunning,
    isPaused,
    progress,
    formattedTime,
    start,
    pause,
    resume,
    reset
  }
}
