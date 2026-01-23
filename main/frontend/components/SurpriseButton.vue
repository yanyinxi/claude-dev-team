<script setup lang="ts">
/**
 * 惊喜按钮组件
 *
 * 功能：
 * - 点击按钮显示随机惊喜内容
 * - 包含励志名言、编程笑话、有趣事实等
 * - 带有动画效果
 */

import { ref, computed } from 'vue'

// =====================================================
// 惊喜内容数据库
// =====================================================

interface Surprise {
  type: 'quote' | 'joke' | 'fact' | 'easter-egg'
  content: string
  emoji: string
  color: string
}

const surprises: Surprise[] = [
  // 励志名言
  {
    type: 'quote',
    content: '代码如诗，每一行都是创造的艺术 ✨',
    emoji: '🎨',
    color: '#667eea'
  },
  {
    type: 'quote',
    content: '今天的 Bug 是明天的经验 💪',
    emoji: '🐛',
    color: '#f093fb'
  },
  {
    type: 'quote',
    content: '优秀的程序员不是写代码最多的，而是删代码最多的 🗑️',
    emoji: '✂️',
    color: '#4facfe'
  },
  {
    type: 'quote',
    content: '学习编程就像健身，坚持才能看到效果 🏋️',
    emoji: '💪',
    color: '#43e97b'
  },

  // 编程笑话
  {
    type: 'joke',
    content: '为什么程序员总是分不清万圣节和圣诞节？\n因为 Oct 31 == Dec 25 😄',
    emoji: '🎃',
    color: '#fa709a'
  },
  {
    type: 'joke',
    content: '程序员的三大谎言：\n1. 代码写完了\n2. 测试通过了\n3. 文档已更新 😂',
    emoji: '🤥',
    color: '#fee140'
  },
  {
    type: 'joke',
    content: 'Bug：我是一个特性！\n特性：我是一个 Bug！\n程序员：都是文档没写清楚 📝',
    emoji: '🐞',
    color: '#30cfd0'
  },

  // 有趣事实
  {
    type: 'fact',
    content: '世界上第一个程序员是女性：Ada Lovelace 👩‍💻',
    emoji: '👩‍💻',
    color: '#a8edea'
  },
  {
    type: 'fact',
    content: 'Python 的名字来自英国喜剧团体 Monty Python 🐍',
    emoji: '🐍',
    color: '#fed6e3'
  },
  {
    type: 'fact',
    content: '第一个计算机 Bug 是真的虫子（飞蛾）🦋',
    emoji: '🦋',
    color: '#c471f5'
  },

  // 彩蛋消息
  {
    type: 'easter-egg',
    content: '🎉 恭喜你发现了隐藏彩蛋！\n你获得了"好奇宝宝"称号 🏆',
    emoji: '🎁',
    color: '#fa709a'
  },
  {
    type: 'easter-egg',
    content: '✨ 魔法时刻！\n你的代码今天会特别顺利 🍀',
    emoji: '🔮',
    color: '#667eea'
  },
  {
    type: 'easter-egg',
    content: '🌟 今日幸运数字：42\n（《银河系漫游指南》中宇宙的终极答案）',
    emoji: '🚀',
    color: '#4facfe'
  }
]

// =====================================================
// 响应式数据
// =====================================================

const currentSurprise = ref<Surprise | null>(null)
const isAnimating = ref(false)
const showSurprise = ref(false)
const clickCount = ref(0)

// =====================================================
// 计算属性
// =====================================================

const buttonText = computed(() => {
  if (clickCount.value === 0) return '🎁 点我有惊喜'
  if (clickCount.value < 3) return '🎉 再来一次'
  if (clickCount.value < 5) return '✨ 还有更多'
  if (clickCount.value < 10) return '🌟 停不下来'
  return '🚀 惊喜大师'
})

const surpriseTypeLabel = computed(() => {
  if (!currentSurprise.value) return ''

  const labels = {
    quote: '💡 励志名言',
    joke: '😄 编程笑话',
    fact: '📚 有趣事实',
    'easter-egg': '🎁 隐藏彩蛋'
  }

  return labels[currentSurprise.value.type]
})

// =====================================================
// 方法
// =====================================================

/**
 * 获取随机惊喜 - 核心逻辑
 *
 * 业务流程：
 * 1. 随机选择一个惊喜
 * 2. 避免连续两次相同
 * 3. 增加点击计数
 */
const getRandomSurprise = (): Surprise => {
  let newSurprise: Surprise

  // 避免连续两次相同的惊喜
  do {
    const randomIndex = Math.floor(Math.random() * surprises.length)
    newSurprise = surprises[randomIndex]
  } while (currentSurprise.value && newSurprise.content === currentSurprise.value.content)

  return newSurprise
}

/**
 * 处理按钮点击 - 核心交互方法
 *
 * 业务流程：
 * 1. 触发动画
 * 2. 获取随机惊喜
 * 3. 显示惊喜内容
 * 4. 增加点击计数
 */
const handleClick = () => {
  // 如果正在动画中，忽略点击
  if (isAnimating.value) return

  // 开始动画
  isAnimating.value = true
  showSurprise.value = false

  // 延迟显示新惊喜（等待淡出动画）
  setTimeout(() => {
    currentSurprise.value = getRandomSurprise()
    showSurprise.value = true
    clickCount.value++

    // 动画结束
    setTimeout(() => {
      isAnimating.value = false
    }, 300)
  }, 200)
}

/**
 * 关闭惊喜弹窗
 */
const closeSurprise = () => {
  showSurprise.value = false
  currentSurprise.value = null
}
</script>

<template>
  <div class="surprise-button-container">
    <!-- 惊喜按钮 -->
    <button
      class="surprise-button"
      :class="{ 'animating': isAnimating }"
      @click="handleClick"
    >
      <span class="button-text">{{ buttonText }}</span>
      <span class="click-count" v-if="clickCount > 0">{{ clickCount }}</span>
    </button>

    <!-- 惊喜弹窗 -->
    <Transition name="surprise">
      <div
        v-if="showSurprise && currentSurprise"
        class="surprise-modal"
        @click="closeSurprise"
      >
        <div
          class="surprise-content"
          :style="{ borderColor: currentSurprise.color }"
          @click.stop
        >
          <!-- 关闭按钮 -->
          <button class="close-button" @click="closeSurprise">✕</button>

          <!-- 惊喜类型标签 -->
          <div class="surprise-type" :style="{ backgroundColor: currentSurprise.color }">
            {{ surpriseTypeLabel }}
          </div>

          <!-- 惊喜 emoji -->
          <div class="surprise-emoji">{{ currentSurprise.emoji }}</div>

          <!-- 惊喜内容 -->
          <div class="surprise-text">{{ currentSurprise.content }}</div>

          <!-- 操作按钮 -->
          <div class="surprise-actions">
            <button
              class="action-button primary"
              :style="{ backgroundColor: currentSurprise.color }"
              @click="handleClick"
            >
              🎲 再来一个
            </button>
            <button
              class="action-button secondary"
              @click="closeSurprise"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* ===================================================== */
/* 惊喜按钮样式 */
/* ===================================================== */

.surprise-button-container {
  display: inline-block;
  position: relative;
}

.surprise-button {
  position: relative;
  padding: 12px 32px;
  font-size: 18px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  overflow: hidden;
}

.surprise-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.surprise-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.surprise-button:active::before {
  width: 300px;
  height: 300px;
}

.surprise-button.animating {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px) rotate(-5deg); }
  75% { transform: translateX(10px) rotate(5deg); }
}

.button-text {
  position: relative;
  z-index: 1;
}

.click-count {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: #ff6b6b;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* ===================================================== */
/* 惊喜弹窗样式 */
/* ===================================================== */

.surprise-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.surprise-content {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 4px solid;
  animation: bounceIn 0.5s ease-out;
}

@keyframes bounceIn {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.close-button {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  font-size: 18px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  background: #e0e0e0;
  transform: rotate(90deg);
}

.surprise-type {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
}

.surprise-emoji {
  font-size: 80px;
  margin-bottom: 20px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.surprise-text {
  font-size: 18px;
  line-height: 1.6;
  color: #2c3e50;
  margin-bottom: 30px;
  white-space: pre-line;
}

.surprise-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.action-button {
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button.primary {
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.action-button.secondary {
  background: #f0f0f0;
  color: #666;
}

.action-button.secondary:hover {
  background: #e0e0e0;
}

/* ===================================================== */
/* 过渡动画 */
/* ===================================================== */

.surprise-enter-active,
.surprise-leave-active {
  transition: opacity 0.3s ease;
}

.surprise-enter-from,
.surprise-leave-to {
  opacity: 0;
}

/* ===================================================== */
/* 响应式设计 */
/* ===================================================== */

@media (max-width: 768px) {
  .surprise-button {
    padding: 10px 24px;
    font-size: 16px;
  }

  .surprise-content {
    padding: 32px 24px;
    max-width: 90%;
  }

  .surprise-emoji {
    font-size: 60px;
  }

  .surprise-text {
    font-size: 16px;
  }

  .surprise-actions {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
  }
}
</style>
