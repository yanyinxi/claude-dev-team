import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const PROGRESS_STORAGE_KEY = 'ket_progress_info'

export const useProgressStore = defineStore('progress', () => {
  const totalQuestions = ref(0)
  const correctAnswers = ref(0)
  const streak = ref(0)
  const dailyGoal = ref(20)
  const completedToday = ref(0)

  function saveToStorage() {
    const progressData = {
      totalQuestions: totalQuestions.value,
      correctAnswers: correctAnswers.value,
      streak: streak.value,
      dailyGoal: dailyGoal.value,
      completedToday: completedToday.value
    }
    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progressData))
  }

  watch([totalQuestions, correctAnswers, streak, dailyGoal, completedToday], () => {
    saveToStorage()
  })

  function restoreProgress() {
    const saved = localStorage.getItem(PROGRESS_STORAGE_KEY)
    if (saved) {
      try {
        const data = JSON.parse(saved)
        totalQuestions.value = data.totalQuestions || 0
        correctAnswers.value = data.correctAnswers || 0
        streak.value = data.streak || 0
        dailyGoal.value = data.dailyGoal || 20
        completedToday.value = data.completedToday || 0
      } catch (e) {
        console.error('恢复进度失败:', e)
      }
    }
  }

  function incrementTotal() {
    totalQuestions.value++
    completedToday.value++
  }

  function incrementCorrect() {
    correctAnswers.value++
    streak.value++
  }

  function resetStreak() {
    streak.value = 0
  }

  function setStreak(value: number) {
    streak.value = value
  }

  function updateProgress(data: any) {
    totalQuestions.value = data.totalQuestions || 0
    correctAnswers.value = data.correctAnswers || 0
    streak.value = data.streak || 0
    dailyGoal.value = data.dailyGoal || 20
    completedToday.value = data.completedToday || 0
  }

  restoreProgress()

  return {
    totalQuestions,
    correctAnswers,
    streak,
    dailyGoal,
    completedToday,
    incrementTotal,
    incrementCorrect,
    resetStreak,
    setStreak,
    updateProgress,
    restoreProgress
  }
})
