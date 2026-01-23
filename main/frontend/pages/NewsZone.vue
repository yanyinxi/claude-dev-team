<script setup lang="ts">
/**
 * 新闻区域页面
 *
 * 功能：
 * - 展示 AI 日报内容
 * - 显示最新的科技资讯
 * - 支持查看历史日报
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getLatestDigest, type AiDigestResponse } from '@/services/aiDigestService'

const router = useRouter()

// 响应式数据
const digest = ref<AiDigestResponse | null>(null)
const loading = ref(true)
const error = ref('')

// 加载最新日报
const loadLatestDigest = async () => {
  try {
    loading.value = true
    error.value = ''
    digest.value = await getLatestDigest()
  } catch (err: any) {
    error.value = err.response?.data?.detail || '加载失败，请稍后重试'
    console.error('加载 AI 日报失败:', err)
  } finally {
    loading.value = false
  }
}

// 返回主页
const goBack = () => {
  router.push('/')
}

// 查看完整日报
const viewFullDigest = () => {
  if (digest.value) {
    router.push(`/ai-digest/${digest.value.date}`)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadLatestDigest()
})
</script>

<template>
  <div class="news-zone">
    <!-- 顶部导航 -->
    <header class="zone-header">
      <div class="container">
        <button @click="goBack" class="back-button">
          <span class="back-icon">←</span>
          <span>返回主页</span>
        </button>
        <h1 class="zone-title">
          <span class="title-icon">📰</span>
          新闻区域
        </h1>
        <button @click="loadLatestDigest" class="refresh-button" :disabled="loading">
          <span v-if="loading" class="spinner">⏳</span>
          <span v-else>🔄</span>
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="news-content">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner-large"></div>
          <p>加载中...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-state">
          <div class="error-icon">⚠️</div>
          <p class="error-message">{{ error }}</p>
          <button @click="loadLatestDigest" class="retry-button">重试</button>
        </div>

        <!-- 日报内容 -->
        <div v-else-if="digest" class="digest-container">
          <!-- 日报头部 -->
          <div class="digest-header">
            <h2 class="digest-title">
              <span class="title-icon">🤖</span>
              今日 AI 要闻
            </h2>
            <span class="digest-date">{{ digest.date }}</span>
          </div>

          <!-- 日报摘要 -->
          <div class="digest-summary">
            <div
              v-for="(item, index) in digest.summary"
              :key="index"
              class="summary-item"
            >
              <div class="item-number">{{ index + 1 }}</div>
              <div class="item-content">
                <a :href="item.url" target="_blank" rel="noopener" class="item-title">
                  {{ item.title }}
                </a>
                <p class="item-description">{{ item.description }}</p>
              </div>
            </div>
          </div>

          <!-- 查看完整日报 -->
          <div class="digest-footer">
            <button @click="viewFullDigest" class="view-full-button">
              查看完整日报 →
            </button>
          </div>
        </div>

        <!-- 无数据状态 -->
        <div v-else class="no-data-state">
          <div class="no-data-icon">📭</div>
          <p>暂无日报数据</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.news-zone {
  min-height: 100vh;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

.back-button,
.refresh-button {
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

.back-button:hover,
.refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
}

.back-button:hover {
  transform: translateX(-4px);
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.back-icon {
  font-size: 20px;
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

/* 主内容区 */
.news-content {
  padding: 60px 0;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 80px 0;
  color: white;
}

.spinner-large {
  width: 60px;
  height: 60px;
  border: 6px solid rgba(255, 255, 255, 0.3);
  border-top: 6px solid white;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

.loading-state p {
  font-size: 18px;
  margin: 0;
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 80px 0;
  color: white;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.error-message {
  font-size: 18px;
  margin: 0 0 24px 0;
}

.retry-button {
  padding: 12px 32px;
  background: white;
  color: #f5576c;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* 日报容器 */
.digest-container {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* 日报头部 */
.digest-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 32px;
}

.digest-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.digest-date {
  font-size: 16px;
  color: #7f8c8d;
  font-weight: 500;
}

/* 日报摘要 */
.digest-summary {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.summary-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.summary-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.item-number {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

.item-content {
  flex: 1;
}

.item-title {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  text-decoration: none;
  margin-bottom: 8px;
  line-height: 1.5;
  transition: color 0.2s ease;
}

.item-title:hover {
  color: #f5576c;
}

.item-description {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.6;
  margin: 0;
}

/* 日报底部 */
.digest-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 2px solid #f0f0f0;
}

.view-full-button {
  padding: 14px 40px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-full-button:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(245, 87, 108, 0.4);
}

/* 无数据状态 */
.no-data-state {
  text-align: center;
  padding: 80px 0;
  color: white;
}

.no-data-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.no-data-state p {
  font-size: 18px;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .zone-header .container {
    flex-wrap: wrap;
    gap: 12px;
  }

  .zone-title {
    font-size: 24px;
    order: 1;
    width: 100%;
    justify-content: center;
  }

  .back-button {
    order: 2;
  }

  .refresh-button {
    order: 3;
  }

  .digest-container {
    padding: 24px;
  }

  .digest-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .digest-title {
    font-size: 24px;
  }

  .summary-item {
    flex-direction: column;
    gap: 12px;
  }

  .item-number {
    align-self: flex-start;
  }

  .item-title {
    font-size: 16px;
  }
}
</style>
