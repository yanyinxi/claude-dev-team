<script setup lang="ts">
/**
 * 主页组件 - 功能区域导航页面
 *
 * 功能：
 * - 展示 4 个功能区域卡片（学习、游戏、新闻、监控）
 * - 点击卡片进入对应的详细页面
 * - 美观的卡片式布局，适合小学生审美
 */

import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

// 功能区域配置
const zones = [
  {
    id: 'learning',
    title: '学习区域',
    subtitle: 'Learning Zone',
    description: '开始学习、错题本、抢答模式',
    icon: '📚',
    color: 'from-blue-400 to-blue-600',
    route: '/learning-zone'
  },
  {
    id: 'game',
    title: '游戏区域',
    subtitle: 'Game Zone',
    description: '飞机大战、趣味小游戏',
    icon: '🎮',
    color: 'from-green-400 to-green-600',
    route: '/game-zone'
  },
  {
    id: 'news',
    title: '新闻区域',
    subtitle: 'News Zone',
    description: 'AI 日报、科技资讯',
    icon: '📰',
    color: 'from-yellow-400 to-orange-500',
    route: '/news-zone'
  },
  {
    id: 'monitor',
    title: '监控区域',
    subtitle: 'Monitor Zone',
    description: 'AlphaZero 系统监控',
    icon: '🤖',
    color: 'from-purple-400 to-pink-500',
    route: '/monitor'
  }
]

// 导航到指定区域
const goToZone = (route: string) => {
  router.push(route)
}
</script>

<template>
  <div class="home-page">
    <!-- 顶部欢迎区域 -->
    <header class="welcome-header">
      <div class="container">
        <h1 class="main-title">
          <span class="wave">👋</span>
          欢迎回来，{{ userStore.user?.nickname || '同学' }}！
        </h1>
        <p class="subtitle">选择一个区域开始你的学习之旅</p>
      </div>
    </header>

    <!-- 功能区域卡片 -->
    <main class="zones-container">
      <div class="container">
        <div class="zones-grid">
          <div
            v-for="zone in zones"
            :key="zone.id"
            class="zone-card"
            @click="goToZone(zone.route)"
          >
            <!-- 卡片背景渐变 -->
            <div class="card-gradient" :class="zone.color"></div>

            <!-- 卡片内容 -->
            <div class="card-content">
              <!-- 图标 -->
              <div class="zone-icon">{{ zone.icon }}</div>

              <!-- 标题 -->
              <h2 class="zone-title">{{ zone.title }}</h2>
              <p class="zone-subtitle">{{ zone.subtitle }}</p>

              <!-- 描述 -->
              <p class="zone-description">{{ zone.description }}</p>

              <!-- 进入按钮 -->
              <div class="enter-button">
                <span>进入</span>
                <span class="arrow">→</span>
              </div>
            </div>

            <!-- 装饰元素 -->
            <div class="card-decoration"></div>
          </div>
        </div>
      </div>
    </main>

    <!-- 底部快捷链接 -->
    <footer class="quick-links">
      <div class="container">
        <router-link to="/profile" class="quick-link">
          <span class="link-icon">👤</span>
          <span>个人中心</span>
        </router-link>
        <router-link to="/login" class="quick-link" v-if="!userStore.isLoggedIn">
          <span class="link-icon">🔑</span>
          <span>登录</span>
        </router-link>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 60px;
}

/* 容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 欢迎区域 */
.welcome-header {
  padding: 60px 0 40px;
  text-align: center;
}

.main-title {
  font-size: 48px;
  font-weight: 800;
  color: white;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.wave {
  display: inline-block;
  animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(20deg); }
  75% { transform: rotate(-20deg); }
}

.subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 500;
}

/* 功能区域容器 */
.zones-container {
  padding: 20px 0;
}

.zones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
}

/* 区域卡片 */
.zone-card {
  position: relative;
  background: white;
  border-radius: 24px;
  padding: 40px 32px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.zone-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* 卡片渐变背景 */
.card-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: linear-gradient(135deg, var(--tw-gradient-stops));
  opacity: 0.9;
  transition: height 0.4s ease;
}

.zone-card:hover .card-gradient {
  height: 100%;
  opacity: 0.15;
}

/* 卡片内容 */
.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

/* 图标 */
.zone-icon {
  font-size: 80px;
  margin-bottom: 20px;
  display: inline-block;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.zone-card:hover .zone-icon {
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

/* 标题 */
.zone-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.zone-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 16px 0;
}

/* 描述 */
.zone-description {
  font-size: 16px;
  color: #5a6c7d;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

/* 进入按钮 */
.enter-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.zone-card:hover .enter-button {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.arrow {
  display: inline-block;
  transition: transform 0.3s ease;
}

.zone-card:hover .arrow {
  transform: translateX(4px);
}

/* 装饰元素 */
.card-decoration {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

/* 底部快捷链接 */
.quick-links {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 12px 0;
}

.quick-links .container {
  display: flex;
  justify-content: center;
  gap: 32px;
}

.quick-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.quick-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

.link-icon {
  font-size: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-title {
    font-size: 32px;
    flex-direction: column;
    gap: 8px;
  }

  .subtitle {
    font-size: 16px;
  }

  .zones-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .zone-card {
    padding: 32px 24px;
  }

  .zone-icon {
    font-size: 64px;
  }

  .zone-title {
    font-size: 24px;
  }

  .quick-links .container {
    gap: 16px;
  }

  .quick-link {
    font-size: 14px;
  }
}

/* 平板设备 */
@media (min-width: 769px) and (max-width: 1024px) {
  .zones-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
