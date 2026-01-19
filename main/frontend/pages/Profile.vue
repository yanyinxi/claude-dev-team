<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useProgressStore } from '@/stores/progressStore'
import { questionService } from '@/services/questionService'
import Button from '@/components/common/Button.vue'
import LearningCalendar from '@/components/common/LearningCalendar.vue'

const router = useRouter()
const userStore = useUserStore()
const progressStore = useProgressStore()

const achievements = ref<any[]>([])
const loading = ref(false)
const studyDates = ref<string[]>([])
const dailyProgress = ref<Record<string, number>>({})
const studyStats = ref({ totalDays: 0, consecutiveDays: 0 })

const accuracy = computed(() => {
  if (progressStore.totalQuestions === 0) return 0
  return Math.round((progressStore.correctAnswers / progressStore.totalQuestions) * 100)
})

async function loadData() {
  loading.value = true
  try {
    const [progressRes, achievementsRes, studyRecordsRes] = await Promise.all([
      questionService.getProgress(),
      questionService.getAchievements(),
      questionService.getStudyRecords()
    ])
    progressStore.updateProgress(progressRes)
    achievements.value = achievementsRes
    studyDates.value = studyRecordsRes.records.map(record => record.date)
    dailyProgress.value = studyRecordsRes.records.reduce((acc, record) => {
      acc[record.date] = record.questionsCompleted
      return acc
    }, {} as Record<string, number>)
    studyStats.value = {
      totalDays: studyRecordsRes.totalDays,
      consecutiveDays: studyRecordsRes.consecutiveDays
    }
  } catch (err) {
    console.error('Failed to load profile data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="min-h-screen p-4 bg-gradient-to-br from-pink-300 via-purple-300 to-indigo-300">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-10 left-10 text-5xl animate-bounce">🎨</div>
      <div class="absolute top-20 right-20 text-4xl animate-pulse">💎</div>
      <div class="absolute bottom-20 left-20 text-4xl animate-bounce delay-100">🌟</div>
      <div class="absolute bottom-10 right-10 text-5xl animate-pulse delay-200">🎪</div>
    </div>

    <div class="max-w-4xl mx-auto relative z-10">
      <div class="flex justify-between items-center mb-6 bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-2xl">
        <div class="flex items-center gap-3">
          <span class="text-5xl animate-bounce">👤</span>
          <h1 class="text-4xl font-black bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            个人主页
          </h1>
        </div>
        <div class="flex gap-3">
          <Button
            variant="secondary"
            class="text-lg py-3 px-6 rounded-2xl font-bold shadow-lg transform transition hover:scale-105"
            @click="router.push('/learning')"
          >
            <span class="mr-2">📚</span>继续学习
          </Button>
          <Button
            variant="secondary"
            class="text-lg py-3 px-6 rounded-2xl font-bold shadow-lg transform transition hover:scale-105"
            @click="router.push('/wrong-book')"
          >
            <span class="mr-2">📝</span>错题本
          </Button>
          <Button
            variant="secondary"
            class="text-lg py-3 px-6 rounded-2xl font-bold shadow-lg transform transition hover:scale-105"
            @click="userStore.logout(); router.push('/login')"
          >
            <span class="mr-2">👋</span>退出
          </Button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-20 bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl">
        <div class="text-7xl mb-4 animate-bounce">⏳</div>
        <p class="text-3xl font-bold text-gray-600">加载中...</p>
      </div>

      <div v-else class="space-y-6">
        <div class="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-4 mb-6">
            <span class="text-6xl">😊</span>
            <div>
              <h2 class="text-3xl font-black text-white mb-2">基本信息</h2>
            </div>
          </div>
          <div class="bg-white/90 rounded-2xl p-6 space-y-4">
            <div class="flex items-center gap-3">
              <span class="text-3xl">🎯</span>
              <p class="text-2xl font-bold text-gray-700">昵称：<span class="text-blue-600">{{ userStore.nickname }}</span></p>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-3xl">🏆</span>
              <p class="text-2xl font-bold text-gray-700">总积分：<span class="text-orange-600">{{ userStore.totalScore }}</span></p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-blue-400 to-cyan-400 rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-4 mb-6">
            <span class="text-6xl">📊</span>
            <h2 class="text-3xl font-black text-white">学习进度</h2>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white/90 rounded-2xl p-6 text-center transform transition hover:scale-105 shadow-lg">
              <div class="text-5xl mb-3">📝</div>
              <p class="text-4xl font-black text-blue-600 mb-2">{{ progressStore.totalQuestions }}</p>
              <p class="text-lg font-bold text-gray-600">总题数</p>
            </div>
            <div class="bg-white/90 rounded-2xl p-6 text-center transform transition hover:scale-105 shadow-lg">
              <div class="text-5xl mb-3">✅</div>
              <p class="text-4xl font-black text-green-600 mb-2">{{ progressStore.correctAnswers }}</p>
              <p class="text-lg font-bold text-gray-600">答对数</p>
            </div>
            <div class="bg-white/90 rounded-2xl p-6 text-center transform transition hover:scale-105 shadow-lg">
              <div class="text-5xl mb-3">🎯</div>
              <p class="text-4xl font-black text-yellow-600 mb-2">{{ accuracy }}%</p>
              <p class="text-lg font-bold text-gray-600">正确率</p>
            </div>
            <div class="bg-white/90 rounded-2xl p-6 text-center transform transition hover:scale-105 shadow-lg">
              <div class="text-5xl mb-3">🔥</div>
              <p class="text-4xl font-black text-red-600 mb-2">{{ progressStore.streak }}</p>
              <p class="text-lg font-bold text-gray-600">连击数</p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-green-400 to-emerald-400 rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-4 mb-6">
            <span class="text-6xl">🎯</span>
            <h2 class="text-3xl font-black text-white">今日目标</h2>
          </div>
          <div class="bg-white/90 rounded-2xl p-6">
            <div class="flex justify-between items-center mb-4">
              <span class="text-2xl font-bold text-gray-700">今日完成</span>
              <span class="text-3xl font-black text-green-600">{{ progressStore.completedToday }} / {{ progressStore.dailyGoal }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-8 shadow-inner">
              <div
                class="bg-gradient-to-r from-green-500 to-emerald-500 h-8 rounded-full transition-all flex items-center justify-end pr-3"
                :style="{ width: `${Math.min((progressStore.completedToday / progressStore.dailyGoal) * 100, 100)}%` }"
              >
                <span v-if="progressStore.completedToday > 0" class="text-white font-black text-lg">
                  {{ Math.round((progressStore.completedToday / progressStore.dailyGoal) * 100) }}%
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 学习日历 -->
        <div class="col-span-2">
          <LearningCalendar
            v-if="studyDates.length > 0"
            :study-dates="studyDates"
            :daily-progress="dailyProgress"
          />
          <div
            v-else
            class="bg-white/90 rounded-3xl p-10 text-center shadow-2xl"
          >
            <div class="text-6xl mb-4">📅</div>
            <p class="text-xl font-bold text-gray-600">暂未获取到学习日历数据</p>
            <p class="text-sm text-gray-500 mt-2">完成几次练习或稍后再试试吧</p>
          </div>
          <div class="grid grid-cols-2 gap-4 mt-4">
            <div class="bg-white/90 rounded-2xl p-6 text-center shadow-lg">
              <p class="text-sm text-gray-500">本月学习天数</p>
              <p class="text-3xl font-black text-blue-600">{{ studyStats.totalDays }}</p>
            </div>
            <div class="bg-white/90 rounded-2xl p-6 text-center shadow-lg">
              <p class="text-sm text-gray-500">连续学习天数</p>
              <p class="text-3xl font-black text-green-600">{{ studyStats.consecutiveDays }}</p>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-r from-purple-400 to-pink-400 rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-4 mb-6">
            <span class="text-6xl">🏅</span>
            <h2 class="text-3xl font-black text-white">成就徽章</h2>
          </div>
          <div v-if="achievements.length === 0" class="bg-white/90 rounded-2xl p-12 text-center">
            <div class="text-7xl mb-4">🎁</div>
            <p class="text-2xl font-bold text-gray-600">暂无成就，继续努力吧！</p>
          </div>
          <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="achievement in achievements"
              :key="achievement.id"
              class="bg-white/90 rounded-2xl p-6 text-center transform transition hover:scale-105 shadow-lg"
              :class="achievement.isUnlocked ? '' : 'opacity-50'"
            >
              <div class="text-6xl mb-3 animate-bounce">{{ achievement.isUnlocked ? '🏆' : '🔒' }}</div>
              <p class="text-xl font-black text-gray-800 mb-2">{{ achievement.name }}</p>
              <p class="text-sm font-medium text-gray-600">{{ achievement.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.delay-100 {
  animation-delay: 0.1s;
}

.delay-200 {
  animation-delay: 0.2s;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
