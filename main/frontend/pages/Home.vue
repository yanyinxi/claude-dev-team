<script setup lang="ts">
/**
 * 主页组件
 *
 * 功能：
 * - 显示 AI 日报卡片
 * - 显示学习入口
 * - 显示 AlphaZero 监控入口
 * - 显示其他功能入口
 */

import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import AiDigestCard from '@/components/AiDigestCard.vue'
import SurpriseButton from '@/components/SurpriseButton.vue'

const router = useRouter()
const userStore = useUserStore()

// 导航到学习页面
const goToLearning = () => {
  router.push('/learning')
}

// 导航到错题本
const goToWrongBook = () => {
  router.push('/wrong-book')
}

// 导航到抢答模式
const goToSpeedQuiz = () => {
  router.push('/speed-quiz')
}

// 导航到个人中心
const goToProfile = () => {
  router.push('/profile')
}

// 导航到 AlphaZero 监控
const goToMonitor = () => {
  router.push('/monitor')
}
</script>

<template>
  <div class="home-page">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="container">
        <h1 class="logo">KET 备考系统</h1>
        <nav class="nav">
          <router-link to="/learning" class="nav-link">学习</router-link>
          <router-link to="/ai-digest" class="nav-link">AI 日报</router-link>
          <router-link to="/monitor" class="nav-link monitor-link">
            🤖 AlphaZero
          </router-link>
          <router-link to="/profile" class="nav-link">个人中心</router-link>
        </nav>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <div class="container">
        <!-- 欢迎信息 -->
        <section class="welcome-section">
          <h2 class="welcome-title">欢迎回来，{{ userStore.user?.nickname || '同学' }}！</h2>
          <p class="welcome-subtitle">继续你的学习之旅</p>
          <!-- 惊喜按钮 -->
          <div class="surprise-button-wrapper">
            <SurpriseButton />
          </div>
        </section>

        <!-- AlphaZero 监控卡片 -->
        <section class="monitor-section">
          <div class="monitor-card" @click="goToMonitor">
            <div class="monitor-content">
              <div class="monitor-icon">🧠</div>
              <div class="monitor-info">
                <h3 class="monitor-title">🤖 AlphaZero 自博弈学习系统</h3>
                <p class="monitor-description">
                  智能策略选择 + 多变体评估 + 持续进化 · 让 AI 团队越用越聪明
                </p>
              </div>
            </div>
            <div class="monitor-arrow">→</div>
          </div>
        </section>

        <!-- AI 日报卡片 -->
        <section class="ai-digest-section">
          <AiDigestCard />
        </section>

        <!-- 功能入口 -->
        <section class="features-section">
          <h3 class="section-title">学习功能</h3>
          <div class="features-grid">
            <div class="feature-card" @click="goToLearning">
              <div class="feature-icon">📚</div>
              <h4 class="feature-title">开始学习</h4>
              <p class="feature-description">词汇、语法、阅读练习</p>
            </div>

            <div class="feature-card" @click="goToWrongBook">
              <div class="feature-icon">📝</div>
              <h4 class="feature-title">错题本</h4>
              <p class="feature-description">复习错题，巩固知识</p>
            </div>

            <div class="feature-card" @click="goToSpeedQuiz">
              <div class="feature-icon">⚡</div>
              <h4 class="feature-title">抢答模式</h4>
              <p class="feature-description">快速答题，挑战自我</p>
            </div>

            <div class="feature-card" @click="goToProfile">
              <div class="feature-icon">👤</div>
              <h4 class="feature-title">个人中心</h4>
              <p class="feature-description">查看学习进度和成就</p>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 顶部导航 */
.header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 16px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.nav {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link:hover {
  opacity: 0.8;
}

.monitor-link {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  padding: 8px 16px;
  border-radius: 20px;
}

/* 主内容区 */
.main-content {
  padding: 40px 0;
}

/* 欢迎信息 */
.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-title {
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
}

.welcome-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

/* 惊喜按钮容器 */
.surprise-button-wrapper {
  margin-top: 24px;
}

/* AlphaZero 监控卡片 */
.monitor-section {
  margin-bottom: 32px;
}

.monitor-card {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border: 2px solid rgba(147, 51, 234, 0.5);
  border-radius: 16px;
  padding: 24px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.monitor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(147, 51, 234, 0.3);
  border-color: rgba(147, 51, 234, 0.8);
}

.monitor-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.monitor-icon {
  font-size: 48px;
}

.monitor-title {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
}

.monitor-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.monitor-arrow {
  font-size: 32px;
  color: rgba(147, 51, 234, 0.8);
  transition: transform 0.3s ease;
}

.monitor-card:hover .monitor-arrow {
  transform: translateX(8px);
}

/* AI 日报区域 */
.ai-digest-section {
  margin-bottom: 40px;
}

/* 功能区域 */
.features-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin: 0 0 24px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.feature-description {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header .container {
    flex-direction: column;
    gap: 16px;
  }

  .nav {
    width: 100%;
    justify-content: center;
  }

  .welcome-title {
    font-size: 28px;
  }

  .monitor-card {
    flex-direction: column;
    text-align: center;
  }

  .monitor-content {
    flex-direction: column;
    text-align: center;
  }

  .monitor-arrow {
    margin-top: 16px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
