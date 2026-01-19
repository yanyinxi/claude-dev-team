<script setup lang="ts">
interface Props {
  score: number
  streak: number
}

defineProps<Props>()
</script>

<template>
  <div class="flex items-center gap-6">
    <div class="flex items-center gap-2 bg-yellow-100 px-4 py-2 rounded-lg">
      <span class="text-2xl">⭐</span>
      <div>
        <p class="text-xs text-gray-600">积分</p>
        <p class="text-lg font-bold text-yellow-600">{{ score }}</p>
      </div>
    </div>

    <div class="flex items-center gap-2 bg-orange-100 px-4 py-2 rounded-lg">
      <span class="text-2xl">🔥</span>
      <div>
        <p class="text-xs text-gray-600">连击</p>
        <p class="text-lg font-bold text-orange-600">{{ streak }}</p>
      </div>
    </div>
  </div>
</template>
