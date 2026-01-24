<!-- =====================================================
知识图谱组件
=====================================================
功能：卡片式展示知识条目，支持搜索和筛选
===================================================== -->

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

const monitorStore = useMonitorStore()

// 搜索关键词
const searchKeyword = ref('')

// 选中的类别
const selectedCategory = ref('all')

// 知识图谱数据
const knowledgeData = computed(() => {
  return monitorStore.knowledgeGraph?.categories || {}
})

// 类别列表
const categories = computed(() => {
  return Object.keys(knowledgeData.value)
})

// 筛选后的知识条目
const filteredKnowledge = computed(() => {
  const data = knowledgeData.value

  if (selectedCategory.value !== 'all') {
    return { [selectedCategory.value]: data[selectedCategory.value] }
  }

  return data
})

// 格式化日期
function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

// 获取类别图标
function getCategoryIcon(category: string) {
  const icons: Record<string, string> = {
    strategy: '🎯',
    'best-practice': '⭐',
    template: '📋',
    'error-handling': '🔧'
  }
  return icons[category] || '📚'
}
</script>

<template>
  <div class="knowledge-graph-container">
    <div class="knowledge-header">
      <h2 class="knowledge-title">📚 知识图谱</h2>
      <div class="knowledge-controls">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索知识..."
          class="search-input"
        />
        <select v-model="selectedCategory" class="category-select">
          <option value="all">全部类型</option>
          <option
            v-for="category in categories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="monitorStore.loading.knowledge" class="loading">
      加载中...
    </div>

    <div v-else-if="categories.length === 0" class="empty">
      暂无知识数据
    </div>

    <div v-else class="knowledge-content">
      <div
        v-for="(categoryData, categoryName) in filteredKnowledge"
        :key="categoryName"
        class="category-section"
      >
        <h3 class="category-title">
          {{ getCategoryIcon(categoryName) }} {{ categoryName }} ({{ categoryData.count }})
        </h3>
        <div class="knowledge-grid">
          <div
            v-for="item in categoryData.items.slice(0, 6)"
            :key="item.id"
            class="knowledge-card"
          >
            <div class="card-title">{{ item.title }}</div>
            <div class="card-description">{{ item.description }}</div>
            <div class="card-footer">
              <span class="card-source">{{ item.source.split('/').pop() }}</span>
              <span class="card-date">{{ formatDate(item.updated_at) }}</span>
            </div>
            <div class="card-tags">
              <span
                v-for="tag in item.tags.slice(0, 3)"
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.knowledge-graph-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.knowledge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.knowledge-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.knowledge-controls {
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  width: 200px;
}

.category-select {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.loading,
.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.category-section {
  margin-bottom: 30px;
}

.category-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.knowledge-card {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s;
  cursor: pointer;
}

.knowledge-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 15px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.card-description {
  font-size: 13px;
  color: #666;
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #888;
  margin-bottom: 10px;
}

.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  padding: 3px 10px;
  background: white;
  border-radius: 12px;
  font-size: 11px;
  color: #667eea;
}
</style>
