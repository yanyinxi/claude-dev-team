<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import type { AlarmRule } from '@/stores/alarmStore'
import * as alarmService from '@/services/alarmService'

// =====================================================
// 闹钟管理页面（管理员）
// 功能：管理全局和个性化学习规则
// =====================================================

const router = useRouter()
const userStore = useUserStore()

// 检查管理员权限
if (userStore.role !== 'admin') {
  router.push('/learning')
}

const rules = ref<AlarmRule[]>([])
const loading = ref(false)
const error = ref('')

// 表单数据
const showCreateForm = ref(false)
const editingRule = ref<AlarmRule | null>(null)
const formData = ref({
  rule_type: 'global' as 'global' | 'personal',
  student_nickname: '',
  study_duration: 25,
  rest_duration: 5
})

// 加载规则列表
async function loadRules() {
  loading.value = true
  error.value = ''
  try {
    rules.value = await alarmService.getAllRules()
  } catch (err: any) {
    error.value = err.message || '加载规则失败'
  } finally {
    loading.value = false
  }
}

// 创建规则
async function handleCreate() {
  if (formData.value.rule_type === 'personal' && !formData.value.student_nickname) {
    error.value = '个性化规则必须指定学生昵称'
    return
  }

  loading.value = true
  error.value = ''
  try {
    await alarmService.createRule({
      rule_type: formData.value.rule_type,
      student_nickname: formData.value.rule_type === 'personal' ? formData.value.student_nickname : undefined,
      study_duration: formData.value.study_duration,
      rest_duration: formData.value.rest_duration
    })
    showCreateForm.value = false
    resetForm()
    await loadRules()
  } catch (err: any) {
    error.value = err.message || '创建规则失败'
  } finally {
    loading.value = false
  }
}

// 更新规则
async function handleUpdate() {
  if (!editingRule.value) return

  loading.value = true
  error.value = ''
  try {
    await alarmService.updateRule(editingRule.value.id, {
      study_duration: formData.value.study_duration,
      rest_duration: formData.value.rest_duration
    })
    editingRule.value = null
    resetForm()
    await loadRules()
  } catch (err: any) {
    error.value = err.message || '更新规则失败'
  } finally {
    loading.value = false
  }
}

// 删除规则
async function handleDelete(id: number) {
  if (!confirm('确定要删除这条规则吗？')) return

  loading.value = true
  error.value = ''
  try {
    await alarmService.deleteRule(id)
    await loadRules()
  } catch (err: any) {
    error.value = err.message || '删除规则失败'
  } finally {
    loading.value = false
  }
}

// 切换规则状态
async function handleToggle(id: number) {
  loading.value = true
  error.value = ''
  try {
    await alarmService.toggleRule(id)
    await loadRules()
  } catch (err: any) {
    error.value = err.message || '切换规则状态失败'
  } finally {
    loading.value = false
  }
}

// 编辑规则
function startEdit(rule: AlarmRule) {
  editingRule.value = rule
  formData.value = {
    rule_type: rule.rule_type,
    student_nickname: rule.student_nickname || '',
    study_duration: rule.study_duration,
    rest_duration: rule.rest_duration
  }
  showCreateForm.value = true
}

// 重置表单
function resetForm() {
  formData.value = {
    rule_type: 'global',
    student_nickname: '',
    study_duration: 25,
    rest_duration: 5
  }
  editingRule.value = null
}

// 取消编辑
function cancelEdit() {
  showCreateForm.value = false
  resetForm()
}

onMounted(() => {
  loadRules()
})
</script>

<template>
  <div class="alarm-management min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">⏰ 学习闹钟管理</h1>
        <p class="text-gray-600">管理全局和个性化学习规则</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>

      <!-- 创建按钮 -->
      <div class="mb-6">
        <button
          @click="showCreateForm = !showCreateForm"
          class="bg-blue-500 text-white font-bold py-3 px-6 rounded-xl hover:bg-blue-600 transition-colors"
        >
          {{ showCreateForm ? '取消' : '+ 创建新规则' }}
        </button>
      </div>

      <!-- 创建/编辑表单 -->
      <div v-if="showCreateForm" class="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">
          {{ editingRule ? '编辑规则' : '创建新规则' }}
        </h3>

        <div class="space-y-4">
          <!-- 规则类型 -->
          <div v-if="!editingRule">
            <label class="block text-sm font-medium text-gray-700 mb-2">规则类型</label>
            <select
              v-model="formData.rule_type"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="global">全局规则</option>
              <option value="personal">个性化规则</option>
            </select>
          </div>

          <!-- 学生昵称 -->
          <div v-if="formData.rule_type === 'personal' && !editingRule">
            <label class="block text-sm font-medium text-gray-700 mb-2">学生昵称</label>
            <input
              v-model="formData.student_nickname"
              type="text"
              placeholder="输入学生昵称"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <!-- 学习时长 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              学习时长（分钟）: {{ formData.study_duration }}
            </label>
            <input
              v-model.number="formData.study_duration"
              type="range"
              min="5"
              max="120"
              step="5"
              class="w-full"
            />
          </div>

          <!-- 休息时长 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              休息时长（分钟）: {{ formData.rest_duration }}
            </label>
            <input
              v-model.number="formData.rest_duration"
              type="range"
              min="1"
              max="60"
              step="1"
              class="w-full"
            />
          </div>

          <!-- 按钮 -->
          <div class="flex gap-3">
            <button
              @click="editingRule ? handleUpdate() : handleCreate()"
              :disabled="loading"
              class="flex-1 bg-blue-500 text-white font-bold py-3 px-6 rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50"
            >
              {{ editingRule ? '更新' : '创建' }}
            </button>
            <button
              @click="cancelEdit"
              class="flex-1 bg-gray-300 text-gray-700 font-bold py-3 px-6 rounded-xl hover:bg-gray-400 transition-colors"
            >
              取消
            </button>
          </div>
        </div>
      </div>

      <!-- 规则列表 -->
      <div class="space-y-4">
        <div v-if="loading && rules.length === 0" class="text-center py-12 text-gray-500">
          加载中...
        </div>

        <div v-else-if="rules.length === 0" class="text-center py-12 text-gray-500">
          暂无规则，点击上方按钮创建
        </div>

        <div
          v-for="rule in rules"
          :key="rule.id"
          class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow"
        >
          <div class="flex items-center justify-between">
            <!-- 规则信息 -->
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <span
                  class="px-3 py-1 rounded-full text-sm font-medium"
                  :class="{
                    'bg-blue-100 text-blue-600': rule.rule_type === 'global',
                    'bg-purple-100 text-purple-600': rule.rule_type === 'personal'
                  }"
                >
                  {{ rule.rule_type === 'global' ? '全局规则' : '个性化规则' }}
                </span>
                <span
                  v-if="rule.student_nickname"
                  class="text-sm text-gray-600"
                >
                  学生: {{ rule.student_nickname }}
                </span>
                <span
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-600': rule.is_active,
                    'bg-gray-100 text-gray-600': !rule.is_active
                  }"
                >
                  {{ rule.is_active ? '启用' : '禁用' }}
                </span>
              </div>
              <div class="text-lg font-medium text-gray-800">
                📚 学习 {{ rule.study_duration }} 分钟 / ☕ 休息 {{ rule.rest_duration }} 分钟
              </div>
              <div class="text-sm text-gray-500 mt-1">
                创建于 {{ new Date(rule.created_at).toLocaleString('zh-CN') }}
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2">
              <button
                @click="handleToggle(rule.id)"
                :disabled="loading"
                class="px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                :class="{
                  'bg-green-100 text-green-600 hover:bg-green-200': !rule.is_active,
                  'bg-gray-100 text-gray-600 hover:bg-gray-200': rule.is_active
                }"
              >
                {{ rule.is_active ? '禁用' : '启用' }}
              </button>
              <button
                @click="startEdit(rule)"
                :disabled="loading"
                class="px-4 py-2 bg-blue-100 text-blue-600 rounded-lg font-medium hover:bg-blue-200 transition-colors disabled:opacity-50"
              >
                编辑
              </button>
              <button
                @click="handleDelete(rule.id)"
                :disabled="loading"
                class="px-4 py-2 bg-red-100 text-red-600 rounded-lg font-medium hover:bg-red-200 transition-colors disabled:opacity-50"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 返回按钮 -->
      <div class="mt-8 text-center">
        <button
          @click="router.push('/admin')"
          class="bg-gray-300 text-gray-700 font-bold py-3 px-8 rounded-xl hover:bg-gray-400 transition-colors"
        >
          返回管理后台
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.alarm-management {
  min-height: 100vh;
}
</style>
