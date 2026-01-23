<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { GameEngine, GameState, type GameStats } from '../utils/gameEngine';

/**
 * 飞机大战游戏组件
 *
 * 功能：
 * 1. 集成游戏引擎
 * 2. 提供游戏控制按钮（开始、暂停、重新开始）
 * 3. 显示游戏统计信息（分数、最高分）
 * 4. 处理游戏状态变化
 */

// 响应式数据
const canvasRef = ref<HTMLCanvasElement | null>(null);
const gameEngine = ref<GameEngine | null>(null);
const gameState = ref<GameState>(GameState.NOT_STARTED);
const stats = ref<GameStats>({
  score: 0,
  highScore: 0,
  enemiesDestroyed: 0,
});

// 游戏状态文本
const stateText = {
  [GameState.NOT_STARTED]: '准备开始',
  [GameState.PLAYING]: '游戏中',
  [GameState.PAUSED]: '已暂停',
  [GameState.GAME_OVER]: '游戏结束',
};

/**
 * 初始化游戏引擎
 */
onMounted(() => {
  if (!canvasRef.value) return;

  // 创建游戏引擎
  gameEngine.value = new GameEngine(canvasRef.value);

  // 设置回调函数
  gameEngine.value.setCallbacks({
    onScoreChange: (newStats) => {
      stats.value = newStats;
    },
    onGameOver: (finalStats) => {
      stats.value = finalStats;
      gameState.value = GameState.GAME_OVER;
    },
  });

  // 加载最高分
  stats.value = gameEngine.value.getStats();

  // 绑定鼠标移动事件
  canvasRef.value.addEventListener('mousemove', handleMouseMove);
});

/**
 * 清理资源
 */
onUnmounted(() => {
  if (gameEngine.value) {
    gameEngine.value.destroy();
  }
  if (canvasRef.value) {
    canvasRef.value.removeEventListener('mousemove', handleMouseMove);
  }
});

/**
 * 开始游戏
 */
const startGame = () => {
  if (!gameEngine.value) return;
  gameEngine.value.start();
  gameState.value = GameState.PLAYING;
};

/**
 * 暂停游戏
 */
const pauseGame = () => {
  if (!gameEngine.value) return;
  gameEngine.value.pause();
  gameState.value = GameState.PAUSED;
};

/**
 * 继续游戏
 */
const resumeGame = () => {
  if (!gameEngine.value) return;
  gameEngine.value.resume();
  gameState.value = GameState.PLAYING;
};

/**
 * 重新开始游戏
 */
const restartGame = () => {
  startGame();
};

/**
 * 处理鼠标移动
 */
const handleMouseMove = (event: MouseEvent) => {
  if (!gameEngine.value || !canvasRef.value) return;

  const rect = canvasRef.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  gameEngine.value.handleMouseMove(x);
};
</script>

<template>
  <div class="plane-game">
    <!-- 游戏标题 -->
    <div class="game-header">
      <h2 class="game-title">✈️ 飞机大战</h2>
      <div class="game-stats">
        <div class="stat-item">
          <span class="stat-label">分数:</span>
          <span class="stat-value">{{ stats.score }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">最高分:</span>
          <span class="stat-value high-score">{{ stats.highScore }}</span>
        </div>
      </div>
    </div>

    <!-- 游戏画布 -->
    <div class="game-canvas-container">
      <canvas
        ref="canvasRef"
        width="800"
        height="600"
        class="game-canvas"
      ></canvas>

      <!-- 游戏状态遮罩 -->
      <div
        v-if="gameState !== GameState.PLAYING"
        class="game-overlay"
      >
        <div class="overlay-content">
          <!-- 未开始状态 -->
          <div v-if="gameState === GameState.NOT_STARTED" class="overlay-message">
            <h3 class="overlay-title">欢迎来到飞机大战！</h3>
            <div class="game-instructions">
              <p>🎮 操作说明：</p>
              <p>• 使用 ← → 方向键或鼠标移动飞机</p>
              <p>• 飞机会自动发射子弹</p>
              <p>• 击落敌机获得分数</p>
              <p>• 避免与敌机相撞</p>
            </div>
            <button @click="startGame" class="game-button start-button">
              🚀 开始游戏
            </button>
          </div>

          <!-- 暂停状态 -->
          <div v-else-if="gameState === GameState.PAUSED" class="overlay-message">
            <h3 class="overlay-title">游戏已暂停</h3>
            <p class="current-score">当前分数: {{ stats.score }}</p>
            <button @click="resumeGame" class="game-button resume-button">
              ▶️ 继续游戏
            </button>
          </div>

          <!-- 游戏结束状态 -->
          <div v-else-if="gameState === GameState.GAME_OVER" class="overlay-message">
            <h3 class="overlay-title">游戏结束！</h3>
            <div class="final-stats">
              <p class="final-score">最终分数: <strong>{{ stats.score }}</strong></p>
              <p class="enemies-destroyed">击落敌机: <strong>{{ stats.enemiesDestroyed }}</strong></p>
              <p v-if="stats.score === stats.highScore && stats.score > 0" class="new-record">
                🎉 恭喜！创造新纪录！
              </p>
            </div>
            <button @click="restartGame" class="game-button restart-button">
              🔄 重新开始
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 游戏控制按钮 -->
    <div class="game-controls">
      <button
        v-if="gameState === GameState.PLAYING"
        @click="pauseGame"
        class="control-button pause-button"
      >
        ⏸️ 暂停
      </button>
      <button
        v-if="gameState === GameState.PLAYING"
        @click="restartGame"
        class="control-button restart-button"
      >
        🔄 重新开始
      </button>
    </div>
  </div>
</template>

<style scoped>
.plane-game {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.game-header {
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.game-title {
  font-size: 32px;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.game-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.stat-value.high-score {
  color: #ffd700;
}

.game-canvas-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.game-canvas {
  display: block;
  background: #87ceeb;
}

.game-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}

.overlay-content {
  text-align: center;
  color: #ffffff;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.overlay-title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.game-instructions {
  text-align: left;
  margin: 20px 0;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}

.game-instructions p {
  margin: 8px 0;
  font-size: 16px;
  line-height: 1.6;
}

.current-score {
  font-size: 24px;
  margin: 20px 0;
}

.final-stats {
  margin: 20px 0;
}

.final-stats p {
  font-size: 20px;
  margin: 10px 0;
}

.final-score strong,
.enemies-destroyed strong {
  color: #ffd700;
  font-size: 28px;
}

.new-record {
  color: #ffd700;
  font-size: 24px;
  font-weight: bold;
  margin-top: 20px;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.game-button {
  padding: 16px 40px;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  margin-top: 20px;
}

.game-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.game-button:active {
  transform: translateY(0);
}

.start-button {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.resume-button {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.restart-button {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.game-controls {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.control-button {
  padding: 12px 30px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.control-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.control-button:active {
  transform: translateY(0);
}
</style>
