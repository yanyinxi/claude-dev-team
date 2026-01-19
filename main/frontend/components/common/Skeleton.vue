<script setup lang="ts">
// =====================================================
// 骨架屏加载组件
// 功能：显示加载中的占位符，提升用户体验
// =====================================================

interface Props {
  rows?: number
  showAvatar?: boolean
  showTitle?: boolean
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  rows: 4,
  showAvatar: true,
  showTitle: true,
  showActions: true
})
</script>

<template>
  <div class="animate-pulse space-y-4 p-4">
    <!-- 头部区域 -->
    <div class="flex items-center gap-4 mb-6">
      <div
        v-if="showAvatar"
        class="w-16 h-16 bg-gray-200 rounded-full"
      />
      <div class="flex-1 space-y-2">
        <div
          v-if="showTitle"
          class="h-6 bg-gray-200 rounded w-1/3"
        />
        <div class="h-4 bg-gray-200 rounded w-1/4" />
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="space-y-3">
      <div
        v-for="i in rows"
        :key="i"
        class="h-20 bg-gray-200 rounded-2xl"
      />
    </div>

    <!-- 操作按钮区域 -->
    <div
      v-if="showActions"
      class="flex gap-3 mt-6"
    >
      <div class="h-12 bg-gray-200 rounded-xl flex-1" />
      <div class="h-12 bg-gray-200 rounded-xl flex-1" />
    </div>
  </div>
</template>
