import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './styles/tailwind.css'
import './styles/global.css'

// =====================================================
// 应用入口文件
// 职责：初始化 Vue 应用、Pinia、Router
// =====================================================

const app = createApp(App)

// 初始化 Pinia 状态管理
const pinia = createPinia()
app.use(pinia)

// 重要注释：在路由初始化后恢复登录状态
// 确保 Pinia store 已初始化
import { useUserStore } from '@/stores/userStore'
const userStore = useUserStore()
userStore.restoreSession()

// 初始化路由
app.use(router)

// 挂载应用
app.mount('#app')

console.log('🚀 KET备考系统已启动')
