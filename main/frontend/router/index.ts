import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/pages/Home.vue'),
      meta: { requiresAuth: false }  // 首页不需要登录
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
    },
    {
      path: '/ai-digest',
      name: 'AiDigest',
      component: () => import('@/pages/AiDigestPage.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/ai-digest/:date',
      name: 'AiDigestDetail',
      component: () => import('@/pages/AiDigestPage.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach((to, _from, next) => {
  // 路由守卫：需要登录的页面如果未登录则跳转到登录页
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/learning')
  } else {
    next()
  }
})

export default router
