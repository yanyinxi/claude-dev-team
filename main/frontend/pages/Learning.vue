<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useQuestionStore } from '@/stores/questionStore'
import { useProgressStore } from '@/stores/progressStore'
import { useAlarmStore } from '@/stores/alarmStore'
import { questionService } from '@/services/questionService'
import * as alarmService from '@/services/alarmService'
import AnswerOptions from '@/components/learning/AnswerOptions.vue'
import RewardAnimation from '@/components/learning/RewardAnimation.vue'
import AlarmCountdown from '@/components/AlarmCountdown.vue'
import RestPrompt from '@/components/RestPrompt.vue'
import Button from '@/components/common/Button.vue'
import SpeedQuiz from './SpeedQuiz.vue'

const router = useRouter()
const userStore = useUserStore()
const questionStore = useQuestionStore()
const progressStore = useProgressStore()
const alarmStore = useAlarmStore()

const showModeSelection = ref(true)
const selectedMode = ref('')
const loading = ref(false)
const selectedAnswer = ref('')
const showResult = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')
const explanation = ref('')
const showReward = ref(false)
const startTime = ref(0)

// 闹钟相关状态
const alarmLoading = ref(false)
const alarmError = ref('')
const alarmStatusTimer = ref<number | null>(null)

// 加载闹钟状态
async function loadAlarmStatus() {
  try {
    const status = await alarmService.getAlarmStatus()
    alarmStore.updateStatus(status)
  } catch (err: any) {
    console.error('Failed to load alarm status:', err)
  }
}

// 开始学习（启动闹钟）
async function startLearning() {
  alarmLoading.value = true
  alarmError.value = ''
  try {
    const status = await alarmService.startAlarm()
    alarmStore.updateStatus(status)
  } catch (err: any) {
    alarmError.value = err.message || '启动学习失败'
  } finally {
    alarmLoading.value = false
  }
}

// 验证是否可以操作
async function validateOperation() {
  try {
    const validation = await alarmService.validateAlarm()
    alarmStore.updateValidation(validation)
    return validation.can_operate
  } catch (err: any) {
    console.error('Failed to validate operation:', err)
    return true  // 验证失败时允许操作
  }
}

// 定期同步闹钟状态（每 30 秒）
function startAlarmStatusSync() {
  if (alarmStatusTimer.value) {
    clearInterval(alarmStatusTimer.value)
  }
  alarmStatusTimer.value = window.setInterval(() => {
    loadAlarmStatus()
  }, 30000)  // 30 秒
}

// 停止状态同步
function stopAlarmStatusSync() {
  if (alarmStatusTimer.value) {
    clearInterval(alarmStatusTimer.value)
    alarmStatusTimer.value = null
  }
}


const moduleNames = {
  vocabulary: { name: '词汇', emoji: '📚', color: 'from-blue-400 to-cyan-400' },
  grammar: { name: '语法', emoji: '✏️', color: 'from-purple-400 to-pink-400' },
  reading: { name: '阅读', emoji: '📖', color: 'from-green-400 to-teal-400' }
}

async function loadQuestion() {
  // 验证是否可以操作
  const canOperate = await validateOperation()
  if (!canOperate) {
    alarmError.value = alarmStore.validation.reason || '休息时间不能答题'
    return
  }

  loading.value = true
  try {
    const res = await questionService.getRandomQuestion()
    questionStore.setCurrentQuestion(res)
    selectedAnswer.value = ''
    showResult.value = false
    correctAnswer.value = ''
    explanation.value = ''
    startTime.value = Date.now()
  } catch (err) {
    console.error('Failed to load question:', err)
  } finally {
    loading.value = false
  }
}

async function selectMode(mode: string) {
  selectedMode.value = mode
  showModeSelection.value = false
  
  // 启动学习闹钟
  if (alarmStore.isIdle) {
    await startLearning()
  }
  
  if (mode === 'normal') {
    loadQuestion()
  }
}

function backToModeSelection() {
  showModeSelection.value = true
  selectedMode.value = ''
}

async function handleSubmit() {
  if (!selectedAnswer.value || !questionStore.currentQuestion) return

  const answerTime = Math.floor((Date.now() - startTime.value) / 1000)

  try {
    const res = await questionService.submitAnswer(
      questionStore.currentQuestion.id,
      selectedAnswer.value,
      answerTime
    )

    isCorrect.value = res.isCorrect
    correctAnswer.value = res.correctAnswer
    explanation.value = res.explanation ?? ''
    showResult.value = true

    progressStore.incrementTotal()
    if (res.isCorrect) {
      progressStore.incrementCorrect()
      progressStore.setStreak(res.streak)
      userStore.totalScore = res.totalScore
      showReward.value = true
      setTimeout(() => {
        showReward.value = false
      }, 2000)
    } else {
      progressStore.resetStreak()
      if (questionStore.currentQuestion) {
        questionStore.addWrongQuestion(questionStore.currentQuestion, {
          correctAnswer: res.correctAnswer,
          explanation: res.explanation
        })
      }
    }
  } catch (err) {
    console.error('Failed to submit answer:', err)
  }
}

function nextQuestion() {
  loadQuestion()
}

onMounted(() => {
  // 加载闹钟状态
  loadAlarmStatus()
  // 启动状态同步
  startAlarmStatusSync()
})

onUnmounted(() => {
  // 停止状态同步
  stopAlarmStatusSync()
})
</script>

<template>
  <div class="min-h-screen p-3 bg-gradient-to-br from-yellow-300 via-green-300 to-blue-300">
    <!-- 装饰性图标 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-10 left-10 text-3xl animate-bounce">🌈</div>
      <div class="absolute top-20 right-20 text-2xl animate-pulse">⭐</div>
      <div class="absolute bottom-20 left-20 text-2xl animate-bounce delay-100">🎯</div>
      <div class="absolute bottom-10 right-10 text-3xl animate-pulse delay-200">🚀</div>
    </div>

    <div class="max-w-5xl mx-auto relative z-10">
      <!-- 顶部导航栏 - 紧凑设计 -->
      <div class="flex justify-between items-center mb-3 bg-white/90 backdrop-blur-sm rounded-2xl p-3 shadow-xl">
        <div class="flex items-center gap-2">
          <button v-if="!showModeSelection && selectedMode" @click="backToModeSelection" class="text-2xl hover:scale-110 transition">
            ⬅️
          </button>
          <span class="text-2xl">📖</span>
          <h1 class="text-xl font-black bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            学习模式
          </h1>
        </div>
        <div class="flex gap-2 items-center">
          <div class="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-xl px-3 py-1.5 shadow-lg">
            <div class="flex items-center gap-1">
              <span class="text-lg">🏆</span>
              <span class="text-base font-black text-white">{{ userStore.totalScore }}</span>
            </div>
          </div>
          <div class="bg-gradient-to-r from-pink-400 to-purple-400 rounded-xl px-3 py-1.5 shadow-lg">
            <div class="flex items-center gap-1">
              <span class="text-lg">🔥</span>
              <span class="text-base font-black text-white">{{ progressStore.streak }}</span>
            </div>
          </div>
          <Button
            variant="secondary"
            class="text-sm py-1.5 px-3 rounded-xl font-bold shadow-lg"
            @click="router.push('/profile')"
          >
            👤
          </Button>
          <Button
            v-if="userStore.user?.role === 'admin'"
            variant="secondary"
            class="text-sm py-1.5 px-3 rounded-xl font-bold shadow-lg"
            @click="router.push('/admin')"
          >
            ⚙️
          </Button>
          <Button
            variant="secondary"
            class="text-sm py-1.5 px-3 rounded-xl font-bold shadow-lg"
            @click="userStore.logout(); router.push('/login')"
          >
            👋
          </Button>
        </div>
      </div>


      <!-- 闹钟倒计时 -->
      <div v-if="!showModeSelection && selectedMode === 'normal'" class="mb-3">
        <AlarmCountdown />
      </div>

      <!-- 闹钟错误提示 -->
      <div v-if="alarmError" class="mb-3 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl">
        {{ alarmError }}
      </div>


      <!-- 模式选择界面 -->
      <div v-if="showModeSelection" class="bg-white/90 backdrop-blur-sm rounded-2xl p-8 shadow-xl">
        <h2 class="text-2xl font-black text-center mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          选择学习模式
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 普通练习 -->
          <button
            @click="selectMode('normal')"
            class="group bg-gradient-to-br from-blue-400 to-cyan-400 rounded-2xl p-6 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            <div class="text-5xl mb-3">📚</div>
            <h3 class="text-2xl font-black text-white mb-2">普通练习</h3>
            <p class="text-white/90 text-sm">按照自己的节奏学习，巩固知识点</p>
          </button>

          <!-- 人机抢答 -->
          <button
            @click="selectMode('speed-quiz')"
            class="group bg-gradient-to-br from-red-400 to-pink-400 rounded-2xl p-6 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            <div class="text-5xl mb-3">🏆</div>
            <h3 class="text-2xl font-black text-white mb-2">人机抢答</h3>
            <p class="text-white/90 text-sm">与AI机器人竞速答题，挑战自我</p>
          </button>
        </div>
      </div>

      <!-- 人机抢答模式 -->
      <SpeedQuiz v-else-if="selectedMode === 'speed-quiz'" />

      <!-- 普通练习模式 -->
      <div v-else-if="selectedMode === 'normal'" class="bg-white/90 backdrop-blur-sm rounded-2xl p-4 shadow-xl">
        <!-- 进度信息 - 紧凑显示 -->
        <div class="flex justify-between items-center mb-3">
          <div class="flex items-center gap-2">
            <div class="bg-blue-100 rounded-xl px-3 py-1.5">
              <span class="text-sm font-bold text-blue-600">
                📝 第 {{ progressStore.totalQuestions + 1 }} 题
              </span>
            </div>
            <div class="bg-green-100 rounded-xl px-3 py-1.5">
              <span class="text-sm font-bold text-green-600">
                ✅ {{ progressStore.totalQuestions > 0 ? Math.round((progressStore.correctAnswers / progressStore.totalQuestions) * 100) : 0 }}%
              </span>
            </div>
          </div>
        </div>

        <div v-if="loading" class="text-center py-10">
          <div class="text-4xl mb-2 animate-bounce">⏳</div>
          <p class="text-lg font-bold text-gray-600">加载中...</p>
        </div>

        <div v-else-if="questionStore.currentQuestion">
          <!-- 题目卡片 - 紧凑设计 -->
          <div class="mb-3 bg-gradient-to-br from-white to-blue-50 rounded-2xl p-4 shadow-lg border-2 border-blue-200">
            <div class="flex items-center gap-2 mb-2">
              <div :class="`px-3 py-1.5 bg-gradient-to-r ${moduleNames[questionStore.currentQuestion.module as keyof typeof moduleNames].color} text-white rounded-xl text-sm font-black shadow-md flex items-center gap-1`">
                <span class="text-base">{{ moduleNames[questionStore.currentQuestion.module as keyof typeof moduleNames].emoji }}</span>
                <span>{{ moduleNames[questionStore.currentQuestion.module as keyof typeof moduleNames].name }}</span>
              </div>
              <div class="px-3 py-1.5 bg-gradient-to-r from-yellow-400 to-orange-400 text-white rounded-xl text-sm font-black shadow-md flex items-center gap-1">
                <span class="text-base">⭐</span>
                <span>难度 {{ questionStore.currentQuestion.difficulty }}</span>
              </div>
            </div>

            <div class="text-base font-bold mb-2 text-gray-800 leading-relaxed bg-white/70 rounded-xl p-3">
              {{ questionStore.currentQuestion.questionText }}
            </div>

            <img
              v-if="questionStore.currentQuestion.questionImage"
              :src="questionStore.currentQuestion.questionImage"
              alt="题目图片"
              class="max-w-full rounded-xl shadow-lg border-2 border-white"
            />
          </div>

          <!-- 答案选项 -->
          <AnswerOptions
            :question="questionStore.currentQuestion"
            :selected="selectedAnswer"
            :show-result="showResult"
            :correct-answer="correctAnswer"
            @select="selectedAnswer = $event"
          />

          <!-- 结果反馈 - 紧凑设计 -->
          <div v-if="showResult" class="mt-3 p-3 rounded-2xl shadow-lg" :class="isCorrect ? 'bg-gradient-to-r from-green-400 to-emerald-400' : 'bg-gradient-to-r from-red-400 to-pink-400'">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-2xl">{{ isCorrect ? '🎉' : '💪' }}</span>
              <p class="text-lg font-black text-white">
                {{ isCorrect ? '太棒了！答对了！' : '加油！再试一次！' }}
              </p>
            </div>
            <div class="bg-white/90 rounded-xl p-2">
              <p class="text-sm text-gray-700 font-medium">{{ explanation }}</p>
            </div>
          </div>

          <!-- 操作按钮 - 紧凑设计 -->
          <div class="mt-3 flex justify-center">
            <Button
              v-if="!showResult"
              variant="primary"
              size="large"
              class="text-lg py-3 px-8 rounded-2xl font-black shadow-xl transform transition hover:scale-105 bg-gradient-to-r from-blue-500 to-purple-500"
              :disabled="!selectedAnswer"
              @click="handleSubmit"
            >
              <span class="mr-2">✨</span>提交答案
            </Button>
            <Button
              v-else
              variant="primary"
              size="large"
              class="text-lg py-3 px-8 rounded-2xl font-black shadow-xl transform transition hover:scale-105 bg-gradient-to-r from-green-500 to-teal-500"
              @click="nextQuestion"
            >
              <span class="mr-2">➡️</span>下一题
            </Button>
          </div>
        </div>
      </div>
    </div>

    <RewardAnimation v-if="showReward" :streak="progressStore.streak" />
  
    <!-- 休息提示 -->
    <RestPrompt />

  </div>
</template>

<style scoped>
.delay-100 {
  animation-delay: 0.1s;
}

.delay-200 {
  animation-delay: 0.2s;
}
</style>
