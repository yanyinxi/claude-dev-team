<script setup lang="ts">
/**
 * AI 日报卡片组件 - 主页展示
 *
 * 功能：
 * - 显示今日最重要的 3 条 AI 资讯
 * - 点击查看完整日报
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getLatestDigest, type AiDigestResponse } from '@/services/aiDigestService'

// 路由
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
  <div class="ai-digest-card">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadLatestDigest" class="retry-btn">重试</button>
    </div>

    <!-- 日报内容 -->
    <div v-else-if="digest" class="digest-content">
      <!-- 标题 -->
      <div class="header">
        <h2 class="title">
          <span class="icon">🤖</span>
          今日 AI 要闻
        </h2>
        <span class="date">{{ digest.date }}</span>
      </div>

      <!-- 今日最重要的 3 条 -->
      <ul class="summary-list">
        <li
          v-for="(item, index) in digest.summary.slice(0, 3)"
          :key="index"
          class="summary-item"
        >
          <span class="number">{{ index + 1 }}</span>
          <div class="content">
            <a :href="item.url" target="_blank" rel="noopener" class="link">
              {{ item.title }}
            </a>
            <p class="description">{{ item.description }}</p>
          </div>
        </li>
      </ul>

      <!-- 查看完整日报按钮 -->
      <button @click="viewFullDigest" class="view-full-btn">
        查看完整日报 →
      </button>
    </div>

    <!-- 无数据状态 -->
    <div v-else class="no-data">
      <p>暂无日报数据</p>
    </div>
  </div>
</template>

<style scoped>
.ai-digest-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin: 20px 0;
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误状态 */
.error {
  text-align: center;
  padding: 40px 0;
  color: #e74c3c;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.retry-btn:hover {
  background: #2980b9;
}

/* 日报内容 */
.digest-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 16px;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 24px;
}

.date {
  font-size: 14px;
  color: #7f8c8d;
}

/* 摘要列表 */
.summary-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.2s;
}

.summary-item:hover {
  background: #e9ecef;
}

.number {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  background: #3498db;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.content {
  flex: 1;
}

.link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
  line-height: 1.5;
}

.link:hover {
  color: #3498db;
  text-decoration: underline;
}

.description {
  margin: 4px 0 0 0;
  font-size: 13px;
  color: #7f8c8d;
  line-height: 1.4;
}

/* 查看完整日报按钮 */
.view-full-btn {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.view-full-btn:hover {
  background: #2980b9;
}

/* 无数据状态 */
.no-data {
  text-align: center;
  padding: 40px 0;
  color: #95a5a6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ai-digest-card {
    padding: 16px;
    margin: 16px 0;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .title {
    font-size: 18px;
  }

  .summary-item {
    flex-direction: column;
    gap: 8px;
  }

  .number {
    align-self: flex-start;
  }
}
</style>
