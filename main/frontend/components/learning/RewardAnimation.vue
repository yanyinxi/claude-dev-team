<script setup lang="ts">
interface Props {
  streak: number
}

defineProps<Props>()
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center pointer-events-none z-50">
    <div class="animate-bounce">
      <div class="text-8xl">⭐</div>
      <p v-if="streak > 1" class="text-3xl font-bold text-yellow-500 text-center mt-4">
        连击 {{ streak }}!
      </p>
    </div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-bounce {
  animation: bounce 0.5s ease-in-out 3;
}
</style>
