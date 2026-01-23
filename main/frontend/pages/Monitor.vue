<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
    <!-- 头部 -->
    <div class="max-w-7xl mx-auto mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-4xl font-bold text-white mb-2">
            🤖 AlphaZero 监控系统
          </h1>
          <p class="text-purple-300">
            Claude Dev Team 自博弈学习系统运行状态
          </p>
        </div>
        <button
          @click="refreshData"
          :disabled="loading"
          class="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800 
                 text-white rounded-xl font-semibold transition-all flex items-center gap-2"
        >
          <span v-if="loading" class="animate-spin">⏳</span>
          <span v-else>🔄</span>
          {{ loading ? '刷新中...' : '刷新数据' }}
        </button>
      </div>
    </div>

    <!-- 状态概览 -->
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <!-- 系统健康 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <div class="flex items-center gap-3 mb-2">
          <span class="text-3xl">{{ healthData?.status === 'healthy' ? '✅' : '⚠️' }}</span>
          <span class="text-white font-semibold">系统健康</span>
        </div>
        <p class="text-2xl font-bold" :class="healthData?.status === 'healthy' ? 'text-green-400' : 'text-yellow-400'">
          {{ healthData?.status === 'healthy' ? '优秀' : '一般' }}
        </p>
        <p class="text-sm text-gray-400 mt-1">
          最后检查: {{ formatTime(healthData?.timestamp) }}
        </p>
      </div>

      <!-- 经验池 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <div class="flex items-center gap-3 mb-2">
          <span class="text-3xl">📊</span>
          <span class="text-white font-semibold">经验池</span>
        </div>
        <p class="text-2xl font-bold text-cyan-400">{{ stats.experience_count }}</p>
        <p class="text-sm text-gray-400 mt-1">
          平均奖励: {{ stats.avg_reward.toFixed(1) }}/10
        </p>
      </div>

      <!-- Agent 数量 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <div class="flex items-center gap-3 mb-2">
          <span class="text-3xl">👥</span>
          <span class="text-white font-semibold">Agent 数量</span>
        </div>
        <p class="text-2xl font-bold text-yellow-400">{{ stats.agents_count }}</p>
        <p class="text-sm text-gray-400 mt-1">
          策略选择器 + 自博弈训练器
        </p>
      </div>

      <!-- 策略规则 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <div class="flex items-center gap-3 mb-2">
          <span class="text-3xl">📋</span>
          <span class="text-white font-semibold">策略规则</span>
        </div>
        <p class="text-2xl font-bold text-pink-400">{{ stats.rules_count }}</p>
        <p class="text-sm text-gray-400 mt-1">
          实时学习积累
        </p>
      </div>
    </div>

    <!-- 详细数据 -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- 经验池趋势 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          📈 经验池分布
        </h2>
        
        <div v-if="stats.experience_count > 0" class="space-y-4">
          <!-- 按 Agent 分布 -->
          <div>
            <p class="text-sm text-gray-400 mb-2">按 Agent 类型</p>
            <div v-for="(count, agent) in stats.by_agent" :key="agent" class="mb-2">
              <div class="flex justify-between text-white text-sm mb-1">
                <span>{{ formatAgentName(agent) }}</span>
                <span>{{ count }} 条</span>
              </div>
              <div class="h-2 bg-white/20 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all"
                  :style="{ width: `${(count / stats.experience_count) * 100}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-12 text-gray-400">
          <span class="text-4xl mb-4 block">📭</span>
          经验池为空，暂无数据积累
          <p class="text-sm mt-2">执行任务后系统会自动学习</p>
        </div>
      </div>

      <!-- 策略类型分布 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          🎯 策略类型分布
        </h2>
        
        <div v-if="Object.keys(stats.by_keyword).length > 0" class="space-y-3">
          <div v-for="(count, keyword) in stats.by_keyword" :key="keyword" 
               class="flex items-center justify-between p-3 bg-white/5 rounded-xl">
            <div class="flex items-center gap-3">
              <span class="text-2xl">{{ getKeywordEmoji(keyword) }}</span>
              <span class="text-white capitalize">{{ keyword }}</span>
            </div>
            <span class="text-purple-400 font-semibold">{{ count }} 次</span>
          </div>
        </div>
        <div v-else class="text-center py-12 text-gray-400">
          <span class="text-4xl mb-4 block">🎯</span>
          暂无策略分布数据
        </div>
      </div>

      <!-- Agent 列表 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          🤖 Agent 列表
        </h2>
        
        <div class="space-y-2 max-h-80 overflow-y-auto">
          <div v-for="agent in agents" :key="agent.name"
               class="flex items-center justify-between p-3 bg-white/5 rounded-xl hover:bg-white/10 transition-colors">
            <div class="flex items-center gap-3">
              <span class="text-2xl">{{ getAgentEmoji(agent.name) }}</span>
              <div>
                <p class="text-white font-medium">{{ formatAgentName(agent.name) }}</p>
                <p class="text-xs text-gray-400 truncate max-w-[200px]">{{ agent.updated }}</p>
              </div>
            </div>
            <span class="text-xs text-gray-400">{{ formatSize(agent.file_size) }}</span>
          </div>
        </div>
      </div>

      <!-- 策略规则 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          📋 策略规则
        </h2>
        
        <div class="space-y-3">
          <div v-for="rule in rules" :key="rule.name"
               class="p-4 bg-white/5 rounded-xl">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <span class="text-xl">{{ getRuleEmoji(rule.name) }}</span>
                <span class="text-white font-medium capitalize">{{ rule.name }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ rule.updated }}</span>
            </div>
            <div class="flex items-center gap-4 text-sm">
              <span class="text-purple-400">洞察: {{ rule.insights_count }} 条</span>
              <span class="text-gray-400">{{ formatSize(rule.file_size) }}</span>
            </div>
          </div>
          <div v-if="rules.length === 0" class="text-center py-8 text-gray-400">
            暂无策略规则
          </div>
        </div>
      </div>
    </div>

    <!-- 最近经验记录 -->
    <div class="max-w-7xl mx-auto bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
      <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
        📜 最近经验记录
      </h2>
      
      <div v-if="experiencePool.records.length > 0" class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-left text-gray-400 text-sm border-b border-white/20">
              <th class="pb-3">时间</th>
              <th class="pb-3">Agent</th>
              <th class="pb-3">策略</th>
              <th class="pb-3">结果预览</th>
              <th class="pb-3">奖励</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(record, index) in experiencePool.records" :key="index" 
                class="border-b border-white/10 hover:bg-white/5">
              <td class="py-3 text-gray-300 text-sm">{{ formatTime(record.timestamp) }}</td>
              <td class="py-3">
                <span class="text-white">{{ formatAgentName(record.agent) }}</span>
              </td>
              <td class="py-3">
                <span class="px-2 py-1 bg-purple-500/30 text-purple-300 rounded-lg text-xs">
                  {{ record.strategy_keyword }}
                </span>
              </td>
              <td class="py-3 text-gray-400 text-sm truncate max-w-[200px]">
                {{ record.result_preview || '无' }}
              </td>
              <td class="py-3">
                <span class="font-bold" :class="getRewardColor(record.reward)">
                  {{ record.reward.toFixed(1) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center py-12 text-gray-400">
        <span class="text-4xl mb-4 block">📭</span>
        暂无经验记录
        <p class="text-sm mt-2">执行任务后会自动记录学习经验</p>
      </div>
    </div>

    <!-- 底部说明 -->
    <div class="max-w-7xl mx-auto mt-8 text-center text-gray-400 text-sm">
      <p>💡 系统会随着使用越来越聪明 - 经验池和策略规则会持续增长</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  getSystemStats, 
  getAgentsInfo, 
  getRulesInfo, 
  getExperiencePool,
  healthCheck,
  type SystemStats,
  type AgentInfo,
  type RuleInfo,
  type ExperiencePool,
  type HealthCheck
} from '@/services/monitor'

// 数据状态
const loading = ref(true)
const healthData = ref<HealthCheck | null>(null)
const stats = ref<SystemStats>({
  agents_count: 0,
  hooks_count: 0,
  rules_count: 0,
  experience_count: 0,
  avg_reward: 0,
  recent_24h_count: 0,
  by_agent: {},
  by_keyword: {},
  healthy: true
})
const agents = ref<AgentInfo[]>([])
const rules = ref<RuleInfo[]>([])
const experiencePool = ref<ExperiencePool>({
  total: 0,
  records: [],
  avg_reward: 0
})

// 获取所有数据
async function refreshData() {
  loading.value = true
  console.log('开始刷新监控数据...')
  try {
    const [health, systemStats, agentsData, rulesData, experience] = await Promise.all([
      healthCheck(),
      getSystemStats(),
      getAgentsInfo(),
      getRulesInfo(),
      getExperiencePool(20)
    ])
    
    console.log('获取到的数据:', { health, systemStats, agentsData })

    healthData.value = health || { status: 'degraded', checks: {}, timestamp: '' }
    stats.value = systemStats || {
      agents_count: 0,
      hooks_count: 0,
      rules_count: 0,
      experience_count: 0,
      avg_reward: 0,
      recent_24h_count: 0,
      by_agent: {},
      by_keyword: {},
      healthy: false
    }
    agents.value = agentsData || []
    rules.value = rulesData || []
    experiencePool.value = experience || { total: 0, records: [], avg_reward: 0 }
  } catch (error) {
    console.error('获取监控数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化时间
function formatTime(timestamp: string | undefined): string {
  if (!timestamp) return '-'
  try {
    const date = new Date(timestamp)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return '-'
  }
}

// 格式化 Agent 名称
function formatAgentName(name: string): string {
  const names: Record<string, string> = {
    'strategy-selector': '策略选择器',
    'self-play-trainer': '自博弈训练器',
    'evolver': '进化引擎',
    'frontend-developer': '前端开发',
    'backend-developer': '后端开发',
    'orchestrator': '协调器',
    'product-manager': '产品经理',
    'tech-lead': '技术负责人',
    'code-reviewer': '代码审查',
    'test': '测试工程师',
    'progress-viewer': '进度查看'
  }
  return names[name] || name.replace(/-/g, ' ')
}

// 格式化文件大小
function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + 'B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
  return (bytes / 1024 / 1024).toFixed(1) + 'MB'
}

// 获取奖励颜色
function getRewardColor(reward: number): string {
  if (reward >= 8) return 'text-green-400'
  if (reward >= 5) return 'text-yellow-400'
  return 'text-red-400'
}

// 获取关键词 Emoji
function getKeywordEmoji(keyword: string): string {
  const emojis: Record<string, string> = {
    'frontend': '🎨',
    'backend': '⚙️',
    'testing': '🧪',
    'architecture': '🏗️',
    'product': '📦',
    'review': '🔍',
    'general': '📝',
    'authentication': '🔐',
    'user-management': '👤'
  }
  return emojis[keyword] || '📊'
}

// 获取 Agent Emoji
function getAgentEmoji(name: string): string {
  const emojis: Record<string, string> = {
    'strategy-selector': '🎯',
    'self-play-trainer': '🏋️',
    'evolver': '🧬',
    'frontend-developer': '🎨',
    'backend-developer': '⚙️',
    'orchestrator': '🎪',
    'product-manager': '📋',
    'tech-lead': '👨‍💻',
    'code-reviewer': '🔍',
    'test': '🧪',
    'progress-viewer': '📈'
  }
  return emojis[name] || '🤖'
}

// 获取规则 Emoji
function getRuleEmoji(name: string): string {
  const emojis: Record<string, string> = {
    'frontend': '🎨',
    'backend': '⚙️',
    'collaboration': '🤝'
  }
  return emojis[name] || '📋'
}

// 生命周期
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
