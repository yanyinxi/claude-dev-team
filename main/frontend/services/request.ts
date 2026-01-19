import axios from 'axios'
import { useUserStore } from '@/stores/userStore'
import router from '@/router'

// =====================================================
// Axios 实例配置
// =====================================================

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '')

const request = axios.create({
  baseURL: `${apiBaseUrl}`,
  timeout: 10000,
  withCredentials: true
})

// =====================================================
// 请求拦截器 - 自动添加认证 Token
// =====================================================

request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    console.error('请求配置错误:', error)
    return Promise.reject(error)
  }
)

// =====================================================
// 响应拦截器 - 统一错误处理
// =====================================================

request.interceptors.response.use(
  (response) => {
    // 直接返回响应数据
    return response.data
  },
  (error) => {
    if (!window.navigator.onLine) {
      return Promise.reject({
        type: 'network',
        message: '网络连接已断开，请检查网络设置',
        isRetryable: false
      })
    }

    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      return Promise.reject({
        type: 'timeout',
        message: '请求超时，请稍后重试',
        isRetryable: true
      })
    }

    const status = error.response?.status

    if (status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      router.push('/login')
      return Promise.reject({
        type: 'auth',
        message: '登录已过期，请重新登录',
        isRetryable: false
      })
    }

    if (status === 403) {
      return Promise.reject({
        type: 'forbidden',
        message: '您没有权限执行此操作',
        isRetryable: false
      })
    }

    if (status === 404) {
      return Promise.reject({
        type: 'notfound',
        message: '请求的资源不存在',
        isRetryable: false
      })
    }

    if (status === 422) {
      const detail = error.response?.data?.detail
      const message = Array.isArray(detail)
        ? detail.map((d: any) => d.msg).join(', ')
        : detail || '请求数据格式错误'
      return Promise.reject({
        type: 'validation',
        message: `数据验证失败: ${message}`,
        isRetryable: false
      })
    }

    if (status >= 500) {
      return Promise.reject({
        type: 'server',
        message: '服务器错误，请稍后重试',
        isRetryable: true
      })
    }

    const errorMessage = error.response?.data?.message || error.message || '请求失败'
    return Promise.reject({
      type: 'unknown',
      message: errorMessage,
      isRetryable: true
    })
  }
)

export type RequestError = {
  type: 'network' | 'timeout' | 'auth' | 'forbidden' | 'notfound' | 'validation' | 'server' | 'unknown'
  message: string
  isRetryable: boolean
}

export default request
