<script setup lang="ts">
interface Question {
  id: number
  module: string
  difficulty: number
  questionText: string
  questionImage?: string
}

interface Props {
  question: Question
}

defineProps<Props>()

const moduleNames = {
  vocabulary: { name: '词汇', emoji: '📚', color: 'from-blue-400 to-cyan-400' },
  grammar: { name: '语法', emoji: '✏️', color: 'from-purple-400 to-pink-400' },
  reading: { name: '阅读', emoji: '📖', color: 'from-green-400 to-teal-400' }
}
</script>

<template>
  <div class="mb-8 bg-gradient-to-br from-white to-blue-50 rounded-3xl p-8 shadow-2xl border-4 border-blue-200">
    <div class="flex items-center gap-3 mb-6">
      <div :class="`px-6 py-3 bg-gradient-to-r ${moduleNames[question.module as keyof typeof moduleNames].color} text-white rounded-2xl text-lg font-black shadow-lg flex items-center gap-2`">
        <span class="text-2xl">{{ moduleNames[question.module as keyof typeof moduleNames].emoji }}</span>
        <span>{{ moduleNames[question.module as keyof typeof moduleNames].name }}</span>
      </div>
      <div class="px-6 py-3 bg-gradient-to-r from-yellow-400 to-orange-400 text-white rounded-2xl text-lg font-black shadow-lg flex items-center gap-2">
        <span class="text-2xl">⭐</span>
        <span>难度 {{ question.difficulty }}</span>
      </div>
    </div>

    <div class="text-2xl font-bold mb-6 text-gray-800 leading-relaxed bg-white/70 rounded-2xl p-6 shadow-inner">
      {{ question.questionText }}
    </div>

    <img
      v-if="question.questionImage"
      :src="question.questionImage"
      alt="题目图片"
      class="max-w-full rounded-2xl shadow-xl border-4 border-white"
    />
  </div>
</template>
