<script setup lang="ts">
/**
 * 学习区域页面
 *
 * 功能：
 * - 展示学习功能列表（开始学习、错题本、抢答模式、学习进度）
 * - 点击功能卡片进入对应页面
 * - 显示学习统计信息
 */

import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useProgressStore } from '@/stores/progressStore'

const router = useRouter()
const userStore = useUserStore()
const progressStore = useProgressStore()

// 学习功能列表
const learningFeatures = [
  {
    id: 'learning',
    title: '开始学习',
    description: '词汇、语法、阅读练习',
    icon: '📚',
    color: 'from-blue-400 to-blue-600',
    route: '/learning'
  },
  {
    id: 'wrong-book',
    title: '错题本',
    description: '复习错题，巩固知识',
    icon: '📝',
    color: 'from-red-400 to-red-600',
    route: '/wrong-book'
  },
  {
    id: 'speed-quiz',
    title: '抢答模式',
    description: '快速答题，挑战自我',
    icon: '⚡',
    color: 'from-yellow-400 to-orange-500',
    route: '/speed-quiz'
  },
  {
    id: 'profile',
    title: '学习进度',
    description: '查看学习进度和成就',
    icon: '📊',
    color: 'from-green-400 to-green-600',
    route: '/profile'
  }
]

// 返回主页
const goBack = () => {
  router.push('/')
}

// 导航到功能页面
const goToFeature = (route: string) => {
  router.push(route)
}
</script>

<template>
  <div class="learning-zone">
    <!-- 顶部导航 -->
    <header class="zone-header">
      <div class="container">
        <button @click="goBack" class="back-button">
          <span class="back-icon">←</span>
          <span>返回主页</span>
        </button>
        <h1 class="zone-title">
          <span class="title-icon">📚</span>
          学习区域
        </h1>
        <div class="user-info">
          <span class="user-name">{{ userStore.user?.nickname || '同学' }}</span>
        </div>
      </div>
    </header>

    <!-- 学习统计 -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <p class="stat-label">总题数</p>
              <p class="stat-value">{{ progressStore.totalQuestions }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <p class="stat-label">正确数</p>
              <p class="stat-value">{{ progressStore.correctAnswers }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔥</div>
            <div class="stat-content">
              <p class="stat-label">连击数</p>
              <p class="stat-value">{{ progressStore.streak }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <p class="stat-label">积分</p>
              <p class="stat-value">{{ userStore.user?.score || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 学习功能列表 -->
    <main class="features-section">
      <div class="container">
        <h2 class="section-title">选择学习方式</h2>
        <div class="features-grid">
          <div
            v-for="feature in learningFeatures"
            :key="feature.id"
            class="feature-card"
            @click="goToFeature(feature.route)"
          >
            <!-- 卡片背景 -->
            <div class="card-bg" :class="feature.color"></div>

            <!-- 卡片内容 -->
            <div class="card-content">
              <div class="feature-icon">{{ feature.icon }}</div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
              <div class="start-button">
                <span>开始</span>
                <span class="arrow">→</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.learning-zone {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 顶部导航 */
.zone-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px 0;
}

.zone-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(-4px);
}

.back-icon {
  font-size: 20px;
}

.zone-title {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 36px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-name {
  color: white;
  font-size: 16px;
  font-weight: 500;
}

/* 学习统计 */
.stats-section {
  padding: 40px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  font-size: 40px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 4px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

/* 学习功能列表 */
.features-section {
  padding: 20px 0;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0 0 40px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

.feature-card {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
}

.card-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(135deg, var(--tw-gradient-stops));
  opacity: 0.9;
  transition: height 0.3s ease;
}

.feature-card:hover .card-bg {
  height: 100%;
  opacity: 0.1;
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.feature-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.feature-title {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.feature-description {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.start-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.feature-card:hover .start-button {
  transform: scale(1.1);
}

.arrow {
  transition: transform 0.3s ease;
}

.feature-card:hover .arrow {
  transform: translateX(4px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .zone-header .container {
    flex-direction: column;
    gap: 16px;
  }

  .zone-title {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-icon {
    font-size: 32px;
  }

  .stat-value {
    font-size: 20px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
