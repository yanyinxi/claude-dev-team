import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Question, WrongQuestion } from '@/services/questionService'

export const useQuestionStore = defineStore('question', () => {
  const currentQuestion = ref<Question | null>(null)
  const questionHistory = ref<Question[]>([])
  const wrongQuestions = ref<WrongQuestion[]>([])
  const currentModule = ref<'vocabulary' | 'grammar' | 'reading'>('vocabulary')

  function setCurrentQuestion(question: Question) {
    currentQuestion.value = question
    questionHistory.value.push(question)
  }

  function addWrongQuestion(question: Question, details: { correctAnswer: string; explanation?: string }) {
    const existing = wrongQuestions.value.find(q => q.questionId === question.id)
    if (existing) {
      existing.wrongCount += 1
      existing.lastWrongAt = new Date().toISOString()
      existing.explanation = details.explanation ?? existing.explanation
      existing.correctAnswer = details.correctAnswer
      return
    }

    wrongQuestions.value.push({
      id: question.id,
      questionId: question.id,
      questionText: question.questionText,
      questionImage: question.questionImage,
      optionA: question.optionA,
      optionB: question.optionB,
      optionC: question.optionC,
      optionD: question.optionD,
      module: question.module,
      difficulty: question.difficulty,
      correctAnswer: details.correctAnswer,
      explanation: details.explanation,
      wrongCount: 1,
      lastWrongAt: new Date().toISOString()
    })
  }

  function clearCurrentQuestion() {
    currentQuestion.value = null
  }

  function removeWrongQuestion(questionId: number) {
    wrongQuestions.value = wrongQuestions.value.filter(q => q.questionId !== questionId)
  }

  return {
    currentQuestion,
    questionHistory,
    wrongQuestions,
    currentModule,
    setCurrentQuestion,
    addWrongQuestion,
    removeWrongQuestion,
    clearCurrentQuestion
  }
})
