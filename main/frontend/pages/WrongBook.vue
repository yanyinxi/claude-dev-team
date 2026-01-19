<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionStore } from '@/stores/questionStore'
import { questionService } from '@/services/questionService'
import type { WrongQuestion } from '@/services/questionService'
import Button from '@/components/common/Button.vue'
import Skeleton from '@/components/common/Skeleton.vue'

// =====================================================
// 错题本页面
// 功能：展示用户答错的题目，支持复习和重新答题
// =====================================================

const router = useRouter()
const questionStore = useQuestionStore()

const loading = ref(true)
const wrongQuestions = ref<WrongQuestion[]>([])
const selectedQuestion = ref<WrongQuestion | null>(null)
const showAnswer = ref(false)
const currentIndex = ref(0)
const optionKeys = ['A', 'B', 'C', 'D'] as const
type OptionKey = typeof optionKeys[number]

// 加载错题本数据
async function loadWrongQuestions() {
  loading.value = true
  try {
    const res = await questionService.getWrongQuestions()
    wrongQuestions.value = res.items || []
  } catch (err) {
    console.error('加载错题本失败:', err)
    // 使用本地缓存的错题
    wrongQuestions.value = [...questionStore.wrongQuestions]
  } finally {
    loading.value = false
  }
}

// 选择一道错题进行复习
function selectQuestion(question: WrongQuestion, index: number) {
  selectedQuestion.value = question
  currentIndex.value = index
  showAnswer.value = false
}

// 显示答案
function toggleAnswer() {
  showAnswer.value = !showAnswer.value
}

// 从错题本移除（已经掌握）
async function removeFromWrongBook(question: WrongQuestion) {
  try {
    await questionService.removeWrongQuestion(question.id)
  } catch (err) {
    console.error('移除错题失败，使用本地降级:', err)
  }

  wrongQuestions.value = wrongQuestions.value.filter(q => q.id !== question.id)
  questionStore.removeWrongQuestion(question.questionId)
  selectedQuestion.value = null
  showAnswer.value = false
}

// 重新练习这道题
function practiceAgain(question: WrongQuestion) {
  questionStore.setCurrentQuestion({
    id: question.questionId,
    module: question.module,
    difficulty: question.difficulty,
    questionText: question.questionText,
    questionImage: question.questionImage,
    optionA: question.optionA,
    optionB: question.optionB,
    optionC: question.optionC,
    optionD: question.optionD
  })
  router.push('/learning')
}

function getOptionValue(question: WrongQuestion, key: OptionKey) {
  if (key === 'A') return question.optionA
  if (key === 'B') return question.optionB
  if (key === 'C') return question.optionC
  return question.optionD
}

onMounted(() => {
  loadWrongQuestions()
})
</script>

<template>
  <div class="min-h-screen p-4 bg-gradient-to-br from-blue-300 via-purple-300 to-pink-300">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-10 left-10 text-5xl animate-bounce">📚</div>
      <div class="absolute top-20 right-20 text-4xl animate-pulse">✏️</div>
      <div class="absolute bottom-20 left-20 text-4xl animate-bounce delay-100">🎯</div>
      <div class="absolute bottom-10 right-10 text-5xl animate-pulse delay-200">📖</div>
    </div>

    <div class="max-w-4xl mx-auto relative z-10">
      <!-- 头部 -->
      <div class="flex justify-between items-center mb-6 bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-2xl">
        <div class="flex items-center gap-3">
          <span class="text-5xl animate-bounce">📝</span>
          <h1 class="text-4xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            错题本
          </h1>
        </div>
        <div class="flex gap-3">
          <Button
            variant="secondary"
            class="text-lg py-3 px-6 rounded-2xl font-bold shadow-lg"
            @click="router.push('/learning')"
          >
            <span class="mr-2">📚</span>继续学习
          </Button>
          <Button
            variant="secondary"
            class="text-lg py-3 px-6 rounded-2xl font-bold shadow-lg"
            @click="router.push('/profile')"
          >
            <span class="mr-2">👤</span>个人主页
          </Button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="bg-white/90 backdrop-blur-sm rounded-3xl p-8 shadow-2xl">
        <Skeleton :rows="3" />
      </div>

      <!-- 空状态 -->
      <div
        v-else-if="wrongQuestions.length === 0"
        class="bg-white/90 backdrop-blur-sm rounded-3xl p-12 shadow-2xl text-center"
      >
        <div class="text-8xl mb-6 animate-bounce">🎉</div>
        <h2 class="text-3xl font-black text-gray-800 mb-4">太棒了！</h2>
        <p class="text-xl text-gray-600 mb-8">你的错题本是空的，继续保持！</p>
        <Button
          variant="primary"
          size="large"
          class="text-xl py-4 px-8 rounded-2xl font-bold shadow-xl"
          @click="router.push('/learning')"
        >
          <span class="mr-2">🚀</span>开始学习
        </Button>
      </div>

      <!-- 错题列表 -->
      <div v-else class="grid md:grid-cols-2 gap-6">
        <!-- 左侧：错题列表 -->
        <div class="space-y-4">
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-2xl">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">
              📚 共 {{ wrongQuestions.length }} 道错题
            </h2>

            <div class="space-y-3 max-h-[60vh] overflow-y-auto">
              <div
                v-for="(question, index) in wrongQuestions"
                :key="question.id"
                data-testid="wrong-question-item"
                :class="[
                  'p-4 rounded-2xl cursor-pointer transition-all transform hover:scale-102',
                  selectedQuestion?.id === question.id
                    ? 'bg-blue-100 border-2 border-blue-400'
                    : 'bg-gray-50 hover:bg-gray-100'
                ]"
                @click="selectQuestion(question, index)"
              >
                <div class="flex items-center gap-3">
                  <span class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
                    {{ index + 1 }}
                  </span>
                  <div class="flex-1">
                    <p class="font-medium text-gray-800 line-clamp-2">
                      {{ question.questionText }}
                    </p>
                    <div class="flex gap-2 mt-2">
                      <span class="px-2 py-1 bg-blue-100 text-blue-600 rounded-lg text-xs font-medium">
                        {{ question.module }}
                      </span>
                      <span class="px-2 py-1 bg-yellow-100 text-yellow-600 rounded-lg text-xs font-medium">
                        难度 {{ question.difficulty }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：错题详情 -->
        <div v-if="selectedQuestion" class="space-y-4">
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-2xl">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">
              📖 第 {{ currentIndex + 1 }} 题详情
            </h2>

            <div class="space-y-4">
              <!-- 题目内容 -->
              <div class="p-4 bg-gray-50 rounded-2xl">
                <p class="text-lg font-medium text-gray-800">
                  {{ selectedQuestion.questionText }}
                </p>
                <img
                  v-if="selectedQuestion.questionImage"
                  :src="selectedQuestion.questionImage"
                  alt="题目图片"
                  class="mt-4 max-w-full rounded-lg"
                />
              </div>

              <!-- 选项 -->
              <div class="space-y-2">
                <div
                  v-for="option in optionKeys"
                  :key="option"
                  v-show="getOptionValue(selectedQuestion, option)"
                  :class="[
                    'p-4 rounded-2xl font-medium',
                    option === 'A' ? 'bg-red-50' :
                    option === 'B' ? 'bg-blue-50' :
                    option === 'C' ? 'bg-green-50' : 'bg-yellow-50'
                  ]"
                >
                  {{ option }}. {{ getOptionValue(selectedQuestion, option) }}
                </div>
              </div>

              <!-- 答案和解析 -->
              <div v-if="showAnswer" class="p-4 bg-green-100 rounded-2xl">
                <p class="font-bold text-green-800 mb-2">
                  ✅ 正确答案: {{ selectedQuestion.correctAnswer || 'A' }}
                </p>
                <p class="text-gray-700">
                  {{ selectedQuestion.explanation || '这道题考查的是对知识点的理解，请仔细阅读相关章节。' }}
                </p>
              </div>

              <!-- 操作按钮 -->
              <div class="flex gap-3 mt-4">
                <Button
                  variant="primary"
                  class="flex-1 py-3 rounded-xl font-bold"
                  data-testid="toggle-answer"
                  @click="toggleAnswer"
                >
                  {{ showAnswer ? '🙈 隐藏答案' : '👁️ 查看答案' }}
                </Button>
                <Button
                  variant="secondary"
                  class="flex-1 py-3 rounded-xl font-bold"
                  data-testid="practice-btn"
                  @click="practiceAgain(selectedQuestion)"
                >
                  🔄 重新练习
                </Button>
              </div>

              <Button
                variant="danger"
                class="w-full py-3 rounded-xl font-bold"
                data-testid="remove-btn"
                @click="removeFromWrongBook(selectedQuestion)"
              >
                ✅ 已掌握，移出错题本
              </Button>
            </div>
          </div>
        </div>

        <!-- 未选择题目时的提示 -->
        <div v-else class="md:col-span-2 bg-white/90 backdrop-blur-sm rounded-3xl p-12 shadow-2xl text-center">
          <div class="text-6xl mb-4">👈</div>
          <p class="text-xl text-gray-600">从左侧选择一道错题进行复习</p>
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
