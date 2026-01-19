<script setup lang="ts">
interface Props {
  class?: string
}

defineProps<Props>()
</script>

<template>
  <div :class="['bg-white rounded-xl shadow-lg p-6', $props.class]">
    <slot />
  </div>
</template>
