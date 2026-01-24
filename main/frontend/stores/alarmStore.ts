import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export interface AlarmRule {
  id: number
  rule_type: 'global' | 'personal'
  student_nickname: string | null
  study_duration: number
  rest_duration: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface AlarmStatus {
  session_type: 'studying' | 'resting' | 'idle'
  start_time: string | null
  end_time: string | null
  remaining_seconds: number
  is_blocked: boolean
  rule: AlarmRule | null
}

export interface AlarmValidation {
  can_operate: boolean
  reason: string | null
  remaining_seconds: number
}

export const useAlarmStore = defineStore('alarm', () => {
  const status = ref<AlarmStatus>({
    session_type: 'idle',
    start_time: null,
    end_time: null,
    remaining_seconds: 0,
    is_blocked: false,
    rule: null
  })

  const validation = ref<AlarmValidation>({
    can_operate: true,
    reason: null,
    remaining_seconds: 0
  })

  const countdownTimer = ref<number | null>(null)
  const showRestPrompt = ref(false)

  const isStudying = computed(() => status.value.session_type === 'studying')
  const isResting = computed(() => status.value.session_type === 'resting')
  const isIdle = computed(() => status.value.session_type === 'idle')
  const isBlocked = computed(() => status.value.is_blocked)

  const remainingTime = computed(() => {
    const seconds = status.value.remaining_seconds
    const minutes = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  })

  const isWarning = computed(() => {
    return isStudying.value && status.value.remaining_seconds <= 300 && status.value.remaining_seconds > 0
  })

  const progressPercent = computed(() => {
    if (!status.value.rule) return 0
    const totalSeconds = isStudying.value
      ? status.value.rule.study_duration * 60
      : status.value.rule.rest_duration * 60
    const elapsed = totalSeconds - status.value.remaining_seconds
    return Math.min(100, Math.max(0, (elapsed / totalSeconds) * 100))
  })

  function updateStatus(newStatus: AlarmStatus) {
    status.value = newStatus
    if (newStatus.session_type === 'resting' && newStatus.remaining_seconds > 0) {
      showRestPrompt.value = true
    }
    if (newStatus.session_type === 'idle' || newStatus.session_type === 'studying') {
      showRestPrompt.value = false
    }
  }

  function updateValidation(newValidation: AlarmValidation) {
    validation.value = newValidation
  }

  function startCountdown() {
    if (countdownTimer.value) {
      clearInterval(countdownTimer.value)
    }
    countdownTimer.value = window.setInterval(() => {
      if (status.value.remaining_seconds > 0) {
        status.value.remaining_seconds -= 1
        if (isWarning.value && status.value.remaining_seconds % 60 === 0) {
          console.log(`⏰ 警告：还剩 ${Math.floor(status.value.remaining_seconds / 60)} 分钟`)
        }
        if (status.value.remaining_seconds === 0) {
          handleCountdownEnd()
        }
      }
    }, 1000)
  }

  function stopCountdown() {
    if (countdownTimer.value) {
      clearInterval(countdownTimer.value)
      countdownTimer.value = null
    }
  }

  function handleCountdownEnd() {
    if (isStudying.value) {
      showRestPrompt.value = true
      status.value.session_type = 'resting'
      status.value.is_blocked = true
    } else if (isResting.value) {
      showRestPrompt.value = false
      status.value.session_type = 'idle'
      status.value.is_blocked = false
    }
    stopCountdown()
  }

  function closeRestPrompt() {
    showRestPrompt.value = false
  }

  function reset() {
    stopCountdown()
    status.value = {
      session_type: 'idle',
      start_time: null,
      end_time: null,
      remaining_seconds: 0,
      is_blocked: false,
      rule: null
    }
    validation.value = {
      can_operate: true,
      reason: null,
      remaining_seconds: 0
    }
    showRestPrompt.value = false
  }

  watch(() => status.value.session_type, (newType) => {
    if (newType === 'studying' || newType === 'resting') {
      startCountdown()
    } else {
      stopCountdown()
    }
  })

  return {
    status,
    validation,
    showRestPrompt,
    isStudying,
    isResting,
    isIdle,
    isBlocked,
    remainingTime,
    isWarning,
    progressPercent,
    updateStatus,
    updateValidation,
    startCountdown,
    stopCountdown,
    closeRestPrompt,
    reset
  }
})
