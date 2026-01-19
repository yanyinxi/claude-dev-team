<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { authService } from '@/services/authService'
import Button from '@/components/common/Button.vue'
import Card from '@/components/common/Card.vue'

const router = useRouter()
const userStore = useUserStore()

// 网络状态 - 使用 ref 而不是直接访问 navigator
const isOnline = ref(true)

// =====================================================
// 生命周期 - 监听网络状态
// =====================================================

import { onMounted, onUnmounted } from 'vue'

function handleOnline() {
  isOnline.value = true
}

function handleOffline() {
  isOnline.value = false
}

onMounted(() => {
  isOnline.value = navigator.onLine
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})

// =====================================================
// 登录处理函数
// =====================================================

const isAdmin = ref(false)
const nickname = ref('')
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const networkError = ref(false)

// =====================================================
// 核心方法 - 必须定义在模板使用之前
// =====================================================

/**
 * 学生登录处理
 * 必要注释：处理学生快速登录（输入昵称即可）
 */
async function handleStudentLogin() {
  if (!nickname.value.trim()) {
    error.value = '请输入昵称'
    return
  }

  loading.value = true
  error.value = ''
  networkError.value = false

  try {
    const res = await authService.studentLogin(nickname.value)
    userStore.setUser(res.user)
    userStore.setToken(res.token)
    router.push('/learning')
  } catch (err: any) {
    console.error('登录失败:', err)

    if (err.type === 'network') {
      networkError.value = true
      error.value = '网络连接失败，请检查网络后重试'
    } else if (err.type === 'timeout') {
      error.value = '请求超时，请稍后重试'
    } else if (err.type === 'server') {
      error.value = '服务器错误，请稍后重试'
    } else {
      error.value = err.message || '登录失败，请检查账号密码'
    }
  } finally {
    loading.value = false
  }
}

/**
 * 管理员登录处理
 * 必要注释：处理管理员登录（用户名+密码）
 */
async function handleAdminLogin() {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  error.value = ''
  networkError.value = false

  try {
    const res = await authService.adminLogin(username.value, password.value)
    userStore.setUser(res.user)
    userStore.setToken(res.token)
    router.push('/learning')
  } catch (err: any) {
    console.error('管理员登录失败:', err)

    if (err.type === 'network') {
      networkError.value = true
      error.value = '网络连接失败，请检查网络后重试'
    } else if (err.type === 'timeout') {
      error.value = '请求超时，请稍后重试'
    } else if (err.type === 'server') {
      error.value = '服务器错误，请稍后重试'
    } else {
      error.value = err.message || '登录失败，请检查账号密码'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-400 via-purple-400 to-pink-400">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-10 left-10 text-6xl animate-bounce">🌟</div>
      <div class="absolute top-20 right-20 text-5xl animate-pulse">🎈</div>
      <div class="absolute bottom-20 left-20 text-5xl animate-bounce delay-100">🎨</div>
      <div class="absolute bottom-10 right-10 text-6xl animate-pulse delay-200">✨</div>
    </div>

    <Card class="w-full max-w-md relative z-10 bg-white/95 backdrop-blur-sm shadow-2xl">
      <div class="text-center mb-8">
        <div class="text-7xl mb-4 animate-bounce">📚</div>
        <h1 class="text-5xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
          KET备考系统
        </h1>
        <p class="text-xl text-gray-600 font-medium">🚀 快乐学习，轻松备考 🎯</p>
      </div>

      <div class="flex gap-3 mb-8">
        <Button
          :variant="!isAdmin ? 'primary' : 'secondary'"
          class="flex-1 text-lg py-4 rounded-2xl font-bold shadow-lg transform transition hover:scale-105"
          @click="isAdmin = false"
        >
          <span class="mr-2">👦</span>学生登录
        </Button>
        <Button
          :variant="isAdmin ? 'primary' : 'secondary'"
          class="flex-1 text-lg py-4 rounded-2xl font-bold shadow-lg transform transition hover:scale-105"
          @click="isAdmin = true"
        >
          <span class="mr-2">👨‍🏫</span>管理员
        </Button>
      </div>

      <div v-if="!isAdmin" class="space-y-4">
        <div class="relative">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-2xl">😊</span>
          <input
            v-model="nickname"
            type="text"
            placeholder="输入你的昵称"
            class="w-full pl-14 pr-4 py-4 border-3 border-blue-300 rounded-2xl focus:border-blue-500 focus:outline-none text-lg font-medium shadow-md transition"
            @keyup.enter="handleStudentLogin"
          />
        </div>
        <Button
          variant="primary"
          size="large"
          class="w-full text-xl py-5 rounded-2xl font-black shadow-xl transform transition hover:scale-105 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
          :loading="loading"
          @click="handleStudentLogin"
        >
          <span class="mr-2">🎉</span>开始学习
        </Button>
      </div>

      <div v-else class="space-y-4">
        <div class="relative">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-2xl">👤</span>
          <input
            v-model="username"
            type="text"
            placeholder="用户名"
            class="w-full pl-14 pr-4 py-4 border-3 border-purple-300 rounded-2xl focus:border-purple-500 focus:outline-none text-lg font-medium shadow-md transition"
          />
        </div>
        <div class="relative">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-2xl">🔒</span>
          <input
            v-model="password"
            type="password"
            placeholder="密码"
            class="w-full pl-14 pr-4 py-4 border-3 border-purple-300 rounded-2xl focus:border-purple-500 focus:outline-none text-lg font-medium shadow-md transition"
            @keyup.enter="handleAdminLogin"
          />
        </div>
        <Button
          variant="primary"
          size="large"
          class="w-full text-xl py-5 rounded-2xl font-black shadow-xl transform transition hover:scale-105 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
          :loading="loading"
          @click="handleAdminLogin"
        >
          <span class="mr-2">🚪</span>登录
        </Button>
      </div>

      <div v-if="error" class="mt-6 p-4 bg-red-100 border-2 border-red-300 rounded-2xl">
        <p class="text-red-600 text-center font-bold text-lg">
          <span class="mr-2">⚠️</span>{{ error }}
        </p>
        <!-- 网络恢复提示 -->
        <p v-if="networkError" class="text-red-500 text-sm text-center mt-2">
          请检查网络连接后重试
        </p>
      </div>
    </Card>

    <!-- 网络状态检测 -->
    <div
      v-if="!isOnline"
      class="fixed bottom-4 left-1/2 -translate-x-1/2 bg-yellow-500 text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-2"
    >
      <span>📡</span>
      <span class="font-medium">网络连接已断开</span>
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
