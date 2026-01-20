import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/Login.vue')
    },
    {
      path: '/learning',
      name: 'Learning',
      component: () => import('@/pages/Learning.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/pages/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/wrong-book',
      name: 'WrongBook',
      component: () => import('@/pages/WrongBook.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/speed-quiz',
      name: 'SpeedQuiz',
      component: () => import('@/pages/SpeedQuiz.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/pages/Admin.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

router.beforeEach((to, _from, next) => {
  // 核心注释：路由守卫，确保已登录用户才能访问受保护页面
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
