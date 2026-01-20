<template>
  <div>
    <!-- 入口界面 -->
    <div v-if="!store.hasActiveBattle && !showStats" class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
        <h2 class="text-2xl font-bold mb-6">开始抢答</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">难度等级</label>
            <select v-model="difficulty" class="w-full p-3 border rounded-lg">
              <option :value="1">⭐ 简单</option>
              <option :value="2">⭐⭐ 较易</option>
              <option :value="3">⭐⭐⭐ 中等</option>
              <option :value="4">⭐⭐⭐⭐ 较难</option>
              <option :value="5">⭐⭐⭐⭐⭐ 困难</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">题目模块</label>
            <select v-model="module" class="w-full p-3 border rounded-lg">
              <option value="vocabulary">📚 词汇</option>
              <option value="grammar">📝 语法</option>
              <option value="reading">📖 阅读</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">题目数量</label>
            <select v-model="rounds" class="w-full p-3 border rounded-lg">
              <option :value="5">5 题</option>
              <option :value="10">10 题</option>
              <option :value="20">20 题</option>
            </select>
          </div>

          <button
            @click="startBattle"
            :disabled="loading"
            class="w-full bg-blue-500 text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-600 disabled:opacity-50"
          >
            {{ loading ? '准备中...' : '开始抢答' }}
          </button>

          <button
            @click="showStats = true"
            class="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200"
          >
            查看战绩
          </button>
        </div>
      </div>

      <!-- 游戏界面 -->
      <div v-else-if="store.hasActiveBattle" class="space-y-6">
        <!-- 比分 -->
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6">
          <div class="flex justify-between items-center">
            <div class="text-center flex-1">
              <div class="text-3xl font-bold text-blue-600">{{ store.score.user }}</div>
              <div class="text-sm text-gray-600">你</div>
            </div>
            <div class="text-2xl font-bold text-gray-400">VS</div>
            <div class="text-center flex-1">
              <div class="text-3xl font-bold text-red-600">{{ store.score.ai }}</div>
              <div class="text-sm text-gray-600">AI</div>
            </div>
          </div>
        </div>

        <!-- 题目 -->
        <div v-if="store.currentQuestion" class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
          <div class="mb-6">
            <h3 class="text-xl font-bold mb-4">{{ store.currentQuestion.question_text }}</h3>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              v-for="option in options"
              :key="option.key"
              @click="submitAnswer(option.key)"
              :disabled="!store.isAnswering || loading"
              :class="[
                'p-4 rounded-lg text-left font-medium transition-all',
                store.isAnswering && !loading
                  ? 'bg-blue-50 hover:bg-blue-100 border-2 border-blue-200'
                  : 'bg-gray-100 border-2 border-gray-200 cursor-not-allowed'
              ]"
            >
              <span class="font-bold">{{ option.key }}.</span> {{ option.text }}
            </button>
          </div>

          <div v-if="loading" class="mt-6 text-center text-gray-600">
            AI 正在思考中...
          </div>
        </div>

        <!-- 结果 -->
        <div v-if="store.showResult" class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
          <div class="text-center mb-6">
            <div v-if="store.winner === 'user'" class="text-4xl mb-2">🎉</div>
            <div v-else-if="store.winner === 'ai'" class="text-4xl mb-2">😅</div>
            <div v-else class="text-4xl mb-2">🤝</div>

            <h3 class="text-2xl font-bold mb-2">
              {{ store.winner === 'user' ? '你赢了！' : store.winner === 'ai' ? 'AI 赢了' : '平局' }}
            </h3>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-sm text-gray-600 mb-1">你的答案</div>
              <div class="text-2xl font-bold">{{ store.userAnswer }}</div>
              <div class="text-sm text-gray-500">{{ (store.userTime / 1000).toFixed(1) }}秒</div>
            </div>
            <div class="text-center p-4 bg-red-50 rounded-lg">
              <div class="text-sm text-gray-600 mb-1">AI 答案</div>
              <div class="text-2xl font-bold">{{ store.aiAnswer }}</div>
              <div class="text-sm text-gray-500">{{ (store.aiTime / 1000).toFixed(1) }}秒</div>
            </div>
          </div>

          <button
            v-if="hasNextQuestion"
            @click="nextQuestion"
            class="w-full bg-blue-500 text-white py-4 rounded-lg font-bold hover:bg-blue-600"
          >
            下一题
          </button>
          <button
            v-else
            @click="finishBattle"
            class="w-full bg-green-500 text-white py-4 rounded-lg font-bold hover:bg-green-600"
          >
            完成抢答
          </button>
        </div>
      </div>

      <!-- 战绩界面 -->
      <div v-else-if="showStats" class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">我的战绩</h2>
          <button @click="showStats = false" class="text-gray-600 hover:text-gray-800">
            返回
          </button>
        </div>

        <div v-if="store.stats" class="space-y-4">
          <div class="grid grid-cols-3 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-3xl font-bold text-blue-600">{{ store.stats.total_battles }}</div>
              <div class="text-sm text-gray-600">总场次</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-3xl font-bold text-green-600">{{ store.stats.wins }}</div>
              <div class="text-sm text-gray-600">胜场</div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-3xl font-bold text-purple-600">{{ store.winRate }}%</div>
              <div class="text-sm text-gray-600">胜率</div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-yellow-50 rounded-lg">
              <div class="text-2xl font-bold text-yellow-600">{{ (store.stats.fastest_time / 1000).toFixed(1) }}s</div>
              <div class="text-sm text-gray-600">最快答题</div>
            </div>
            <div class="text-center p-4 bg-red-50 rounded-lg">
              <div class="text-2xl font-bold text-red-600">{{ store.stats.max_streak }}</div>
              <div class="text-sm text-gray-600">最长连胜</div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSpeedQuizStore } from '../stores/speedQuizStore'
import { startSpeedQuiz, submitSpeedQuizAnswer, getSpeedQuizStats } from '../services/speedQuizService'

const store = useSpeedQuizStore()

const difficulty = ref(3)
const module = ref('vocabulary')
const rounds = ref(10)
const loading = ref(false)
const showStats = ref(false)
const startTime = ref(0)
const nextQuestionData = ref(null)

const options = computed(() => {
  if (!store.currentQuestion) return []
  return [
    { key: 'A', text: store.currentQuestion.option_a },
    { key: 'B', text: store.currentQuestion.option_b },
    { key: 'C', text: store.currentQuestion.option_c },
    { key: 'D', text: store.currentQuestion.option_d }
  ].filter(opt => opt.text)
})

const hasNextQuestion = computed(() => nextQuestionData.value !== null)

const startBattle = async () => {
  loading.value = true
  try {
    const response = await startSpeedQuiz({
      difficulty: difficulty.value,
      module: module.value,
      rounds: rounds.value
    })
    store.startBattle(response.battle_id, response.question)
    startTime.value = Date.now()
  } catch (error) {
    console.error('开始抢答失败:', error)
    alert('开始抢答失败，请重试')
  } finally {
    loading.value = false
  }
}

const submitAnswer = async (answer: string) => {
  if (!store.isAnswering || loading.value) return

  const answerTime = Date.now() - startTime.value
  store.setUserAnswer(answer, answerTime)
  loading.value = true

  try {
    const response = await submitSpeedQuizAnswer({
      battle_id: store.battleId!,
      question_id: store.currentQuestion!.id,
      answer,
      answer_time: answerTime
    })

    store.setAIAnswer(response.ai_answer, response.ai_time)
    store.setResult(response.winner)
    nextQuestionData.value = response.next_question
  } catch (error) {
    console.error('提交答案失败:', error)
    alert('提交答案失败，请重试')
  } finally {
    loading.value = false
  }
}

const nextQuestion = () => {
  if (nextQuestionData.value) {
    store.setQuestion(nextQuestionData.value)
    nextQuestionData.value = null
    startTime.value = Date.now()
  }
}

const finishBattle = async () => {
  store.endBattle()
  await loadStats()
}

const loadStats = async () => {
  try {
    const stats = await getSpeedQuizStats()
    store.setStats(stats)
  } catch (error) {
    console.error('加载战绩失败:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>
