<script setup lang="ts">
/**
 * 游戏区域页面
 *
 * 功能：
 * - 展示游戏列表（飞机大战游戏）
 * - 预留其他游戏位置
 * - 点击游戏卡片进入游戏
 */

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PlaneGame from '@/components/PlaneGame.vue'

const router = useRouter()

// 是否显示飞机大战游戏
const showPlaneGame = ref(false)

// 游戏列表
const games = [
  {
    id: 'plane-game',
    title: '飞机大战',
    description: '经典飞机射击游戏，挑战你的反应速度',
    icon: '✈️',
    color: 'from-blue-400 to-blue-600',
    available: true
  },
  {
    id: 'word-match',
    title: '单词配对',
    description: '记忆单词，锻炼你的记忆力',
    icon: '🎯',
    color: 'from-green-400 to-green-600',
    available: false
  },
  {
    id: 'grammar-quiz',
    title: '语法挑战',
    description: '快速答题，测试你的语法知识',
    icon: '📝',
    color: 'from-purple-400 to-purple-600',
    available: false
  },
  {
    id: 'reading-race',
    title: '阅读竞赛',
    description: '限时阅读，提升阅读速度',
    icon: '📖',
    color: 'from-orange-400 to-red-500',
    available: false
  }
]

// 返回主页
const goBack = () => {
  router.push('/')
}

// 开始游戏
const startGame = (gameId: string) => {
  if (gameId === 'plane-game') {
    showPlaneGame.value = true
  } else {
    alert('游戏开发中，敬请期待！')
  }
}

// 关闭游戏
const closeGame = () => {
  showPlaneGame.value = false
}
</script>

<template>
  <div class="game-zone">
    <!-- 顶部导航 -->
    <header class="zone-header">
      <div class="container">
        <button @click="goBack" class="back-button">
          <span class="back-icon">←</span>
          <span>返回主页</span>
        </button>
        <h1 class="zone-title">
          <span class="title-icon">🎮</span>
          游戏区域
        </h1>
        <div class="spacer"></div>
      </div>
    </header>

    <!-- 游戏列表 -->
    <main class="games-section" v-if="!showPlaneGame">
      <div class="container">
        <h2 class="section-title">选择一个游戏开始玩吧！</h2>
        <div class="games-grid">
          <div
            v-for="game in games"
            :key="game.id"
            class="game-card"
            :class="{ disabled: !game.available }"
            @click="game.available && startGame(game.id)"
          >
            <!-- 卡片背景 -->
            <div class="card-bg" :class="game.color"></div>

            <!-- 卡片内容 -->
            <div class="card-content">
              <div class="game-icon">{{ game.icon }}</div>
              <h3 class="game-title">{{ game.title }}</h3>
              <p class="game-description">{{ game.description }}</p>

              <!-- 游戏状态 -->
              <div v-if="game.available" class="play-button">
                <span>开始游戏</span>
                <span class="arrow">→</span>
              </div>
              <div v-else class="coming-soon">
                <span>🚧 开发中</span>
              </div>
            </div>

            <!-- 不可用遮罩 -->
            <div v-if="!game.available" class="disabled-overlay"></div>
          </div>
        </div>
      </div>
    </main>

    <!-- 飞机大战游戏 -->
    <div v-if="showPlaneGame" class="game-container">
      <div class="game-header">
        <button @click="closeGame" class="close-button">
          <span>←</span>
          <span>返回游戏列表</span>
        </button>
      </div>
      <PlaneGame />
    </div>
  </div>
</template>

<style scoped>
.game-zone {
  min-height: 100vh;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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

.spacer {
  width: 120px;
}

/* 游戏列表 */
.games-section {
  padding: 60px 0;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0 0 40px 0;
}

.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.game-card {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.game-card:not(.disabled):hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
}

.game-card.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.card-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: linear-gradient(135deg, var(--tw-gradient-stops));
  opacity: 0.9;
  transition: height 0.3s ease;
}

.game-card:not(.disabled):hover .card-bg {
  height: 100%;
  opacity: 0.15;
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.game-icon {
  font-size: 72px;
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.game-card:not(.disabled):hover .game-icon {
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

.game-title {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.game-description {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.play-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.game-card:not(.disabled):hover .play-button {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(17, 153, 142, 0.4);
}

.arrow {
  transition: transform 0.3s ease;
}

.game-card:not(.disabled):hover .arrow {
  transform: translateX(4px);
}

.coming-soon {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: #95a5a6;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
}

.disabled-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.5);
  z-index: 2;
  pointer-events: none;
}

/* 游戏容器 */
.game-container {
  padding: 20px 0;
}

.game-header {
  max-width: 1200px;
  margin: 0 auto 20px;
  padding: 0 24px;
}

.close-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(-4px);
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

  .spacer {
    display: none;
  }

  .games-grid {
    grid-template-columns: 1fr;
  }

  .game-icon {
    font-size: 56px;
  }
}
</style>
