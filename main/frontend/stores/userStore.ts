import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

// =====================================================
// 用户状态管理 Store
// 功能：管理用户登录状态、积分、徽章等
// =====================================================

interface Badge {
  id: number
  name: string
  description: string
  badgeIcon: string
  isUnlocked: boolean
}

// 用户信息本地存储 key
const USER_STORAGE_KEY = 'ket_user_info'

export const useUserStore = defineStore('user', () => {
  // =====================================================
  // 响应式状态
  // =====================================================

  const id = ref<number | null>(null)
  const nickname = ref('')
  const role = ref<'student' | 'admin'>('student')
  const isLoggedIn = ref(false)
  const totalScore = ref(0)
  const badges = ref<Badge[]>([])
  const token = ref('')

  // =====================================================
  // 持久化 - 自动保存用户信息到 localStorage
  // =====================================================

  // 核心注释：使用 Pinia 订阅机制自动同步状态到 localStorage
  function saveToStorage() {
    const userData = {
      id: id.value,
      nickname: nickname.value,
      role: role.value,
      isLoggedIn: isLoggedIn.value,
      totalScore: totalScore.value,
      badges: badges.value,
      token: token.value
    }
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(userData))
  }

  // 监听状态变化，自动保存
  watch([id, nickname, role, isLoggedIn, totalScore, badges, token], () => {
    if (isLoggedIn.value) {
      saveToStorage()
    }
  }, { deep: true })

  // =====================================================
  // 核心方法
  // =====================================================

  /**
   * 设置用户信息 - 登录成功后调用
   * 必要注释：保存用户数据并标记已登录
   */
  function setUser(userData: any) {
    id.value = userData.id
    nickname.value = userData.nickname
    role.value = userData.role || 'student'
    totalScore.value = userData.totalScore || 0
    badges.value = userData.badges || []
    isLoggedIn.value = true
    // Token 单独保存
    if (userData.token) {
      token.value = userData.token
    }
    saveToStorage()
  }

  /**
   * 设置 Token - 登录成功后调用
   * 必要注释：保存 Token 到状态和 localStorage
   */
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('ket_token', newToken)
  }

  /**
   * 退出登录 - 清除所有状态
   * 必要注释：安全退出，清理敏感信息
   */
  function logout() {
    id.value = null
    nickname.value = ''
    role.value = 'student'
    isLoggedIn.value = false
    totalScore.value = 0
    badges.value = []
    token.value = ''
    localStorage.removeItem(USER_STORAGE_KEY)
    localStorage.removeItem('ket_token')
  }

  /**
   * 恢复登录状态 - 页面刷新时调用
   * 重要注释：从 localStorage 恢复用户信息
   */
  function restoreSession() {
    const savedToken = localStorage.getItem('ket_token')
    const savedUser = localStorage.getItem(USER_STORAGE_KEY)

    if (savedToken && savedUser) {
      try {
        const userData = JSON.parse(savedUser)
        token.value = savedToken
        id.value = userData.id
        nickname.value = userData.nickname
        role.value = userData.role
        totalScore.value = userData.totalScore || 0
        badges.value = userData.badges || []
        isLoggedIn.value = true
      } catch (e) {
        console.error('恢复登录状态失败:', e)
        logout()
      }
    }
  }

  /**
   * 更新积分 - 答对题目时调用
   * 重要注释：累加积分，自动保存
   */
  function addScore(points: number) {
    totalScore.value += points
    saveToStorage()
  }

  /**
   * 添加徽章 - 获得成就时调用
   * 重要注释：添加新徽章，去重
   */
  function addBadge(badge: Badge) {
    const exists = badges.value.find(b => b.id === badge.id)
    if (!exists) {
      badges.value.push(badge)
      saveToStorage()
    }
  }

  // =====================================================
  // 导出状态和方法
  // =====================================================

  return {
    id,
    nickname,
    role,
    isLoggedIn,
    totalScore,
    badges,
    token,
    setUser,
    setToken,
    logout,
    restoreSession,
    addScore,
    addBadge
  }
})
