<script setup lang="ts">
/**
 * AI 日报完整页面
 *
 * 功能：
 * - 显示完整的 AI 日报内容
 * - 支持查看历史日报
 * - 分类展示资讯
 */

import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getDigestByDate,
  getLatestDigest,
  getDigestList,
  type AiDigestResponse,
  type AiDigestListItem
} from '@/services/aiDigestService'

// 路由
const route = useRoute()
const router = useRouter()

// 响应式数据
const digest = ref<AiDigestResponse | null>(null)
const historyList = ref<AiDigestListItem[]>([])
const loading = ref(true)
const error = ref('')

// 计算属性：格式化日期
const formattedDate = computed(() => {
  if (!digest.value) return ''
  const date = new Date(digest.value.date)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

// 加载日报
const loadDigest = async (date?: string) => {
  try {
    loading.value = true
    error.value = ''

    if (date) {
      digest.value = await getDigestByDate(date)
    } else {
      digest.value = await getLatestDigest()
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || '加载失败，请稍后重试'
    console.error('加载 AI 日报失败:', err)
  } finally {
    loading.value = false
  }
}

// 加载历史列表
const loadHistory = async () => {
  try {
    historyList.value = await getDigestList(0, 10)
  } catch (err) {
    console.error('加载历史列表失败:', err)
  }
}

// 切换日期
const switchDate = (date: string) => {
  router.push(`/ai-digest/${date}`)
  loadDigest(date)
}

// 组件挂载时加载数据
onMounted(() => {
  const targetDate = route.params.date as string
  loadDigest(targetDate)
  loadHistory()
})
</script>

<template>
  <div class="ai-digest-page">
    <!-- 侧边栏：历史列表 -->
    <aside class="sidebar">
      <h3 class="sidebar-title">历史日报</h3>
      <ul class="history-list">
        <li
          v-for="item in historyList"
          :key="item.id"
          class="history-item"
          :class="{ active: digest?.date === item.date }"
          @click="switchDate(item.date)"
        >
          <span class="date">{{ item.date }}</span>
          <span class="count">{{ item.total_items }} 条</span>
        </li>
      </ul>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadDigest()" class="retry-btn">重试</button>
      </div>

      <!-- 日报内容 -->
      <article v-else-if="digest" class="digest-article">
        <!-- 标题 -->
        <header class="article-header">
          <h1 class="article-title">{{ digest.title }}</h1>
          <p class="article-meta">
            <span class="date">{{ formattedDate }}</span>
            <span class="divider">|</span>
            <span class="count">共 {{ digest.total_items }} 条资讯</span>
          </p>
        </header>

        <!-- 今日要闻 -->
        <section class="section highlights">
          <h2 class="section-title">📌 今日要闻</h2>
          <ul class="highlights-list">
            <li v-for="(item, index) in digest.summary" :key="index" class="highlight-item">
              <span class="number">{{ index + 1 }}</span>
              <div class="content">
                <a :href="item.url" target="_blank" rel="noopener" class="link">
                  {{ item.title }}
                </a>
                <p class="description">{{ item.description }}</p>
              </div>
            </li>
          </ul>
        </section>

        <!-- 分类内容 -->
        <section
          v-for="(category, key) in digest.content"
          :key="key"
          class="section category"
        >
          <h2 class="section-title">{{ getCategoryTitle(key) }}</h2>
          <div class="category-items">
            <div
              v-for="(item, index) in category"
              :key="index"
              class="category-item"
            >
              <h3 class="item-title">
                <a :href="item.url" target="_blank" rel="noopener">
                  {{ item.title }}
                </a>
              </h3>
              <p class="item-description">{{ item.description }}</p>
              <div v-if="item.tags" class="item-tags">
                <span v-for="tag in item.tags" :key="tag" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </section>
      </article>

      <!-- 无数据状态 -->
      <div v-else class="no-data">
        <p>暂无日报数据</p>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
// 获取分类标题
function getCategoryTitle(key: string): string {
  const titles: Record<string, string> = {
    major_releases: '🚀 重大发布',
    agent_tech: '🤖 Agent 技术进展',
    papers: '📊 最新论文',
    open_source: '🛠️ 开源项目',
    breakthroughs: '💡 技术突破',
    industry_news: '💼 行业动态'
  }
  return titles[key] || key
}
</script>

<style scoped>
.ai-digest-page {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: fit-content;
  position: sticky;
  top: 24px;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 16px 0;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-item:hover {
  background: #f8f9fa;
}

.history-item.active {
  background: #3498db;
  color: white;
}

.history-item .date {
  font-size: 14px;
  font-weight: 500;
}

.history-item .count {
  font-size: 12px;
  opacity: 0.8;
}

/* 主内容区 */
.main-content {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 32px;
}

/* 加载和错误状态 */
.loading,
.error,
.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
}

.retry-btn {
  margin-top: 16px;
  padding: 10px 20px;
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

/* 文章内容 */
.digest-article {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.article-header {
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 20px;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.article-meta {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
}

.divider {
  margin: 0 12px;
}

/* 章节 */
.section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

/* 今日要闻 */
.highlights-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.highlight-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.highlight-item .number {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: #3498db;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.highlight-item .content {
  flex: 1;
}

.highlight-item .link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  font-size: 16px;
  line-height: 1.5;
}

.highlight-item .link:hover {
  color: #3498db;
  text-decoration: underline;
}

.highlight-item .description {
  margin: 6px 0 0 0;
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.5;
}

/* 分类内容 */
.category-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.category-item {
  padding: 16px;
  border-left: 3px solid #3498db;
  background: #f8f9fa;
  border-radius: 4px;
}

.item-title {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 8px 0;
}

.item-title a {
  color: #2c3e50;
  text-decoration: none;
}

.item-title a:hover {
  color: #3498db;
  text-decoration: underline;
}

.item-description {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.6;
  margin: 0 0 8px 0;
}

.item-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 8px;
  background: #e9ecef;
  color: #495057;
  border-radius: 4px;
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .ai-digest-page {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    position: static;
  }

  .history-list {
    flex-direction: row;
    overflow-x: auto;
  }

  .history-item {
    flex-shrink: 0;
  }
}

@media (max-width: 768px) {
  .ai-digest-page {
    padding: 16px;
  }

  .main-content {
    padding: 20px;
  }

  .article-title {
    font-size: 24px;
  }

  .section-title {
    font-size: 20px;
  }
}
</style>
