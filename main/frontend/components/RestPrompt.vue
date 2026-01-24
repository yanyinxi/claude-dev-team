<script setup lang="ts">
import { useAlarmStore } from '@/stores/alarmStore'

// =====================================================
// 休息提示组件
// 功能：全屏遮罩，提示休息，建议活动
// =====================================================

const alarmStore = useAlarmStore()

// 休息建议列表
const restSuggestions = [
  { icon: '🚶', text: '站起来走走', description: '活动一下筋骨' },
  { icon: '💧', text: '喝杯水', description: '补充水分' },
  { icon: '👀', text: '看看远处', description: '放松眼睛' },
  { icon: '🧘', text: '深呼吸', description: '放松身心' },
  { icon: '🎵', text: '听听音乐', description: '放松心情' },
  { icon: '🍎', text: '吃点水果', description: '补充能量' }
]

// 随机选择一个建议
const randomSuggestion = restSuggestions[Math.floor(Math.random() * restSuggestions.length)]

// 关闭提示
function handleClose() {
  alarmStore.closeRestPrompt()
}
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="alarmStore.showRestPrompt"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
        @click.self="handleClose"
      >
        <div class="rest-prompt bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full mx-4 animate-bounce-in">
          <!-- 标题 -->
          <div class="text-center mb-6">
            <div class="text-6xl mb-4">⏰</div>
            <h2 class="text-3xl font-bold text-gray-800 mb-2">学习时间到！</h2>
            <p class="text-lg text-gray-600">该休息一下啦~</p>
          </div>

          <!-- 休息倒计时 -->
          <div class="bg-orange-50 rounded-2xl p-6 mb-6 text-center">
            <div class="text-sm text-orange-600 mb-2">休息时间</div>
            <div class="text-5xl font-bold text-orange-500 font-mono">
              {{ alarmStore.remainingTime }}
            </div>
            <div class="mt-4 bg-orange-200 rounded-full h-2 overflow-hidden">
              <div
                class="h-full bg-orange-500 transition-all duration-1000 ease-linear"
                :style="{ width: `${alarmStore.progressPercent}%` }"
              ></div>
            </div>
          </div>

          <!-- 休息建议 -->
          <div class="bg-blue-50 rounded-2xl p-6 mb-6">
            <div class="flex items-center gap-4">
              <div class="text-5xl">{{ randomSuggestion.icon }}</div>
              <div class="flex-1">
                <div class="text-xl font-bold text-gray-800 mb-1">
                  {{ randomSuggestion.text }}
                </div>
                <div class="text-sm text-gray-600">
                  {{ randomSuggestion.description }}
                </div>
              </div>
            </div>
          </div>

          <!-- 提示信息 -->
          <div class="text-center text-sm text-gray-500 mb-6">
            <p>休息时间不能答题哦~</p>
            <p class="mt-1">好好休息，保护眼睛！</p>
          </div>

          <!-- 关闭按钮 -->
          <button
            @click="handleClose"
            class="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white font-bold py-4 px-6 rounded-2xl hover:from-blue-600 hover:to-purple-600 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            知道了
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.rest-prompt {
  animation: bounce-in 0.5s ease-out;
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
