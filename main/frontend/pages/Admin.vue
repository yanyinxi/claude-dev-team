<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

interface Question {
  id: number
  module: string
  difficulty: number
  questionText: string
  optionA: string
  optionB: string
  optionC?: string
  optionD?: string
  correctAnswer: string
  explanation?: string
}

const questions = ref<Question[]>([])
const loading = ref(false)
const editingQuestion = ref<Question | null>(null)
const showEditModal = ref(false)

const moduleNames: Record<string, string> = {
  vocabulary: '词汇',
  grammar: '语法',
  reading: '阅读'
}

onMounted(async () => {
  if (userStore.user?.role !== 'admin') {
    router.push('/learning')
    return
  }
  await loadQuestions()
})

async function loadQuestions() {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/admin/questions', {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    const data = await response.json()
    questions.value = data.map((q: any) => ({
      id: q.id,
      module: q.module,
      difficulty: q.difficulty,
      questionText: q.question_text,
      optionA: q.option_a,
      optionB: q.option_b,
      optionC: q.option_c,
      optionD: q.option_d,
      correctAnswer: q.correct_answer,
      explanation: q.explanation
    }))
  } catch (error) {
    console.error('加载题目失败:', error)
  } finally {
    loading.value = false
  }
}

function editQuestion(question: Question) {
  editingQuestion.value = { ...question }
  showEditModal.value = true
}

async function saveQuestion() {
  if (!editingQuestion.value) return

  loading.value = true
  try {
    const payload = {
      module: editingQuestion.value.module,
      difficulty: editingQuestion.value.difficulty,
      question_text: editingQuestion.value.questionText,
      option_a: editingQuestion.value.optionA,
      option_b: editingQuestion.value.optionB,
      option_c: editingQuestion.value.optionC,
      option_d: editingQuestion.value.optionD,
      correct_answer: editingQuestion.value.correctAnswer,
      explanation: editingQuestion.value.explanation
    }

    await fetch(`http://localhost:8000/api/v1/admin/questions/${editingQuestion.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    showEditModal.value = false
    await loadQuestions()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    loading.value = false
  }
}

async function deleteQuestion(id: number) {
  if (!confirm('确定要删除这道题目吗？')) return

  loading.value = true
  try {
    await fetch(`http://localhost:8000/api/v1/admin/questions/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    await loadQuestions()
  } catch (error) {
    console.error('删除失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-4">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">题库管理</h1>
        <p class="text-gray-600">共 {{ questions.length }} 道题目</p>
      </div>

      <div v-if="loading" class="text-center py-8">
        <div class="text-gray-600">加载中...</div>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="question in questions"
          :key="question.id"
          class="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm font-medium">
                  {{ moduleNames[question.module] }}
                </span>
                <span class="px-2 py-1 bg-purple-100 text-purple-700 rounded text-sm font-medium">
                  难度 {{ question.difficulty }}
                </span>
                <span class="px-2 py-1 bg-green-100 text-green-700 rounded text-sm font-medium">
                  答案: {{ question.correctAnswer }}
                </span>
              </div>
              <p class="text-gray-800 font-medium mb-2">{{ question.questionText }}</p>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>A. {{ question.optionA }}</div>
                <div>B. {{ question.optionB }}</div>
                <div v-if="question.optionC">C. {{ question.optionC }}</div>
                <div v-if="question.optionD">D. {{ question.optionD }}</div>
              </div>
            </div>
            <div class="flex gap-2 ml-4">
              <button
                @click="editQuestion(question)"
                class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
              >
                编辑
              </button>
              <button
                @click="deleteQuestion(question.id)"
                class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div
      v-if="showEditModal && editingQuestion"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold mb-4">编辑题目</h2>

        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium mb-1">模块</label>
            <select v-model="editingQuestion.module" class="w-full p-2 border rounded">
              <option value="vocabulary">词汇</option>
              <option value="grammar">语法</option>
              <option value="reading">阅读</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">难度 (1-5)</label>
            <input v-model.number="editingQuestion.difficulty" type="number" min="1" max="5" class="w-full p-2 border rounded">
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">题目</label>
            <textarea v-model="editingQuestion.questionText" class="w-full p-2 border rounded" rows="3"></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">选项 A</label>
            <input v-model="editingQuestion.optionA" class="w-full p-2 border rounded">
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">选项 B</label>
            <input v-model="editingQuestion.optionB" class="w-full p-2 border rounded">
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">选项 C (可选)</label>
            <input v-model="editingQuestion.optionC" class="w-full p-2 border rounded">
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">选项 D (可选)</label>
            <input v-model="editingQuestion.optionD" class="w-full p-2 border rounded">
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">正确答案</label>
            <select v-model="editingQuestion.correctAnswer" class="w-full p-2 border rounded">
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">解析</label>
            <textarea v-model="editingQuestion.explanation" class="w-full p-2 border rounded" rows="2"></textarea>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button
            @click="saveQuestion"
            class="flex-1 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-medium"
          >
            保存
          </button>
          <button
            @click="showEditModal = false"
            class="flex-1 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-medium"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
