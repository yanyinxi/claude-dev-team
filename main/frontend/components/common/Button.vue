<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'danger'
  size?: 'small' | 'medium' | 'large'
  loading?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  loading: false,
  disabled: false
})

const variantClasses = {
  primary: 'bg-primary hover:bg-blue-600 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
  success: 'bg-success hover:bg-green-600 text-white',
  danger: 'bg-danger hover:bg-red-600 text-white'
}

const sizeClasses = {
  small: 'px-3 py-1 text-sm',
  medium: 'px-4 py-2',
  large: 'px-6 py-3 text-lg'
}
</script>

<template>
  <button
    :class="[
      'rounded-lg font-semibold transition-colors',
      variantClasses[variant],
      sizeClasses[size],
      (disabled || loading) && 'opacity-50 cursor-not-allowed'
    ]"
    :disabled="disabled || loading"
  >
    <span v-if="loading">加载中...</span>
    <slot v-else />
  </button>
</template>
