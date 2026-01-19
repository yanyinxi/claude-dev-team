<script setup lang="ts">
import { computed } from 'vue'
interface Question {
  optionA: string
  optionB: string
  optionC?: string
  optionD?: string
}

interface Props {
  question: Question
  selected: string
  showResult: boolean
  correctAnswer?: string
}

interface Emits {
  (e: 'select', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const options = computed(() => [
  { key: 'A', value: props.question.optionA },
  { key: 'B', value: props.question.optionB },
  { key: 'C', value: props.question.optionC },
  { key: 'D', value: props.question.optionD }
].filter(opt => opt.value))

function getOptionClass(key: string) {
  const base = 'w-full p-4 rounded-xl border-3 text-left transition-all duration-300 cursor-pointer text-base font-bold transform hover:scale-102 shadow-md'

  if (props.showResult) {
    if (key === props.correctAnswer) {
      return `${base} bg-gradient-to-r from-green-400 to-emerald-400 border-green-500 text-white shadow-xl scale-105`
    }
    if (key === props.selected && key !== props.correctAnswer) {
      return `${base} bg-gradient-to-r from-red-400 to-pink-400 border-red-500 text-white shadow-xl`
    }
    return `${base} border-gray-300 opacity-50 cursor-not-allowed`
  }

  if (key === props.selected) {
    return `${base} bg-gradient-to-r from-blue-400 to-purple-400 border-blue-500 text-white shadow-xl scale-105`
  }

  return `${base} bg-white border-gray-300 hover:border-blue-400 hover:bg-blue-50 hover:shadow-lg`
}

function handleSelect(key: string) {
  if (!props.showResult) {
    emit('select', key)
  }
}
</script>

<template>
  <div class="space-y-2 mt-3">
    <button
      v-for="option in options"
      :key="option.key"
      :class="getOptionClass(option.key)"
      @click="handleSelect(option.key)"
      :disabled="showResult"
    >
      <div class="flex items-center">
        <span class="text-xl mr-3 bg-white/30 rounded-full w-8 h-8 flex items-center justify-center font-black">{{ option.key }}</span>
        <span class="text-base">{{ option.value }}</span>
      </div>
    </button>
  </div>
</template>
