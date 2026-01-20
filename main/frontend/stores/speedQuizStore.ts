/**
 * 抢答模式状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Question, SpeedQuizStats } from '../services/speedQuizService'

export const useSpeedQuizStore = defineStore('speedQuiz', () => {
  // 状态
  const battleId = ref<number | null>(null)
  const currentQuestion = ref<Question | null>(null)
  const userAnswer = ref<string | null>(null)
  const userTime = ref<number>(0)
  const aiAnswer = ref<string | null>(null)
  const aiTime = ref<number>(0)
  const score = ref({ user: 0, ai: 0 })
  const isAnswering = ref(false)
  const showResult = ref(false)
  const winner = ref<string | null>(null)
  const stats = ref<SpeedQuizStats | null>(null)

  // 计算属性
  const hasActiveBattle = computed(() => battleId.value !== null)
  const winRate = computed(() => {
    if (!stats.value || stats.value.total_battles === 0) return 0
    return Math.round(stats.value.win_rate * 100)
  })

  // 方法
  const startBattle = (id: number, question: Question) => {
    battleId.value = id
    currentQuestion.value = question
    score.value = { user: 0, ai: 0 }
    resetRound()
  }

  const setQuestion = (question: Question) => {
    currentQuestion.value = question
    resetRound()
  }

  const setUserAnswer = (answer: string, time: number) => {
    userAnswer.value = answer
    userTime.value = time
    isAnswering.value = false
  }

  const setAIAnswer = (answer: string, time: number) => {
    aiAnswer.value = answer
    aiTime.value = time
  }

  const setResult = (winnerValue: string) => {
    winner.value = winnerValue
    showResult.value = true
    if (winnerValue === 'user') {
      score.value.user++
    } else if (winnerValue === 'ai') {
      score.value.ai++
    }
  }

  const resetRound = () => {
    userAnswer.value = null
    userTime.value = 0
    aiAnswer.value = null
    aiTime.value = 0
    isAnswering.value = true
    showResult.value = false
    winner.value = null
  }

  const endBattle = () => {
    battleId.value = null
    currentQuestion.value = null
    resetRound()
    score.value = { user: 0, ai: 0 }
  }

  const setStats = (newStats: SpeedQuizStats) => {
    stats.value = newStats
  }

  return {
    // 状态
    battleId,
    currentQuestion,
    userAnswer,
    userTime,
    aiAnswer,
    aiTime,
    score,
    isAnswering,
    showResult,
    winner,
    stats,
    // 计算属性
    hasActiveBattle,
    winRate,
    // 方法
    startBattle,
    setQuestion,
    setUserAnswer,
    setAIAnswer,
    setResult,
    resetRound,
    endBattle,
    setStats
  }
})
