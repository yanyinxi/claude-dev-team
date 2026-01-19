import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useProgressStore = defineStore('progress', () => {
  const totalQuestions = ref(0)
  const correctAnswers = ref(0)
  const streak = ref(0)
  const dailyGoal = ref(20)
  const completedToday = ref(0)

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

  function updateProgress(data: any) {
    totalQuestions.value = data.totalQuestions || 0
    correctAnswers.value = data.correctAnswers || 0
    streak.value = data.streak || 0
    dailyGoal.value = data.dailyGoal || 20
    completedToday.value = data.completedToday || 0
  }

  return {
    totalQuestions,
    correctAnswers,
    streak,
    dailyGoal,
    completedToday,
    incrementTotal,
    incrementCorrect,
    resetStreak,
    updateProgress
  }
})
