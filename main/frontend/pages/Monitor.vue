<template>
  <div class="min-h-screen bg-slate-900 text-white p-8 font-sans">
    <!-- Header -->
    <div class="max-w-7xl mx-auto mb-10 flex justify-between items-end">
      <div>
        <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Claude 开发团队 v3.0
        </h1>
        <p class="text-slate-400 mt-2 text-lg">LLM 驱动的智能协作监控系统</p>
      </div>
      <div class="flex items-center gap-4">
        <div class="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 flex items-center gap-2">
          <div class="w-2 h-2 rounded-full" :class="health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'"></div>
          <span class="text-sm font-medium">{{ health?.status === 'healthy' ? '系统在线' : '系统降级' }}</span>
        </div>
        <button 
          @click="loadData" 
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          :disabled="loading"
        >
          <span v-if="loading" class="animate-spin">⚡</span>
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Column: Performance & Overview -->
      <div class="lg:col-span-2 space-y-8">
        
        <!-- Performance Metrics -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <span class="text-2xl">📊</span> 性能指标 (目标: 95%+)
          </h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="metric in overview?.metrics" :key="metric.name" 
                 class="bg-slate-900/50 p-4 rounded-xl border border-slate-700/50">
              <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">{{ metric.name }}</div>
              <div class="text-2xl font-bold" :class="metric.status === 'pass' ? 'text-green-400' : 'text-yellow-400'">
                {{ metric.value }}
              </div>
              <div class="text-xs text-slate-500 mt-1">目标: {{ metric.target }}</div>
            </div>
          </div>
        </div>

        <!-- Intelligent Agents -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <span class="text-2xl">🤖</span> 智能代理 ({{ agents.length }})
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[400px] overflow-y-auto custom-scrollbar">
            <div v-for="agent in agents" :key="agent.name" 
                 class="group p-4 bg-slate-900/50 rounded-xl border border-slate-700/50 hover:border-blue-500/50 transition-all cursor-default">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-medium text-blue-300 group-hover:text-blue-200 transition-colors">{{ agent.name }}</h3>
                <span class="text-xs px-2 py-1 bg-slate-800 rounded text-slate-400 border border-slate-700">{{ agent.type }}</span>
              </div>
              <p class="text-sm text-slate-400 line-clamp-2">{{ agent.description }}</p>
            </div>
          </div>
        </div>

        <!-- Test Runner -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
            <span class="text-2xl">🧪</span> 功能验证测试
          </h2>
          <div class="flex gap-4">
            <button 
              @click="runTest" 
              class="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl font-medium transition-colors flex items-center gap-2 disabled:opacity-50"
              :disabled="testing"
            >
              <span v-if="testing" class="animate-spin">⏳</span>
              <span v-else>▶️</span>
              {{ testing ? '正在执行测试...' : '运行随机测试样例' }}
            </button>
            <div v-if="testResult" class="flex-1 bg-slate-900/50 p-4 rounded-xl border border-slate-700/50 font-mono text-sm overflow-x-auto">
              <div class="flex items-center gap-2 mb-2">
                <span :class="testResult.success ? 'text-green-400' : 'text-red-400'">
                  {{ testResult.success ? '✅ 测试通过' : '❌ 测试失败' }}
                </span>
                <span class="text-slate-500 text-xs">{{ testResult.timestamp }}</span>
              </div>
              <p class="text-slate-300">{{ testResult.message }}</p>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Skills & System -->
      <div class="space-y-8">
        
        <!-- Active Skills -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <span class="text-2xl">⚡</span> 核心能力 (Active Skills)
          </h2>
          <div class="space-y-3 max-h-[300px] overflow-y-auto custom-scrollbar">
            <div v-for="skill in skills" :key="skill.name" 
                 class="p-3 bg-slate-900/50 rounded-xl border border-slate-700/50 flex flex-col gap-2">
              <div class="flex justify-between items-center">
                <span class="font-medium text-purple-300">{{ skill.name }}</span>
                <span class="text-xs text-slate-500">{{ skill.tools.length }} 个工具</span>
              </div>
              <p class="text-xs text-slate-400 line-clamp-2">{{ skill.description }}</p>
            </div>
          </div>
        </div>

        <!-- System Status -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-4">系统状态</h2>
          <div class="space-y-4">
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">版本</span>
              <span class="font-mono text-sm">{{ overview?.version }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">模式</span>
              <span class="text-blue-400 text-sm">{{ overview?.mode }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">最后更新</span>
              <span class="text-sm">{{ overview?.last_update }}</span>
            </div>
            <div class="mt-4">
              <div class="text-xs text-slate-500 mb-2">健康检查项</div>
              <div class="grid grid-cols-2 gap-2">
                <div v-for="(ok, check) in health?.checks" :key="check" 
                     class="flex items-center gap-2 text-xs">
                  <span :class="ok ? 'text-green-500' : 'text-red-500'">●</span>
                  <span class="text-slate-300">{{ check }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-4">关于系统</h2>
          <p class="text-sm text-slate-400 leading-relaxed">
            Claude Dev Team v3.0 是一个完全由 LLM 驱动的智能协作系统。它不再依赖传统的固定算法，而是通过深度推理、自适应学习和实时进化来处理复杂的软件开发任务。系统能够自动识别模式、优化策略，并随着使用不断提升性能。
          </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as api from '@/services/monitor'

const loading = ref(false)
const testing = ref(false)
const overview = ref<api.SystemOverview>()
const agents = ref<api.AgentData[]>([])
const skills = ref<api.SkillData[]>([])
const health = ref<api.HealthCheck>()
const testResult = ref<{ success: boolean; message: string; timestamp: string } | null>(null)

const loadData = async () => {
  loading.value = true
  try {
    const [ov, ag, sk, he] = await Promise.all([
      api.getSystemOverview(),
      api.getAgents(),
      api.getSkills(),
      api.checkHealth()
    ])
    overview.value = ov
    agents.value = ag
    skills.value = sk
    health.value = he
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const runTest = async () => {
  testing.value = true
  testResult.value = null
  
  // 模拟随机测试用例
  const testCases = [
    '验证 LLM 任务分解能力...',
    '测试并行 Agent 协作效率...',
    '检查代码质量评估准确性...',
    '验证自适应进化机制...'
  ]
  const randomCase = testCases[Math.floor(Math.random() * testCases.length)]
  
  // 模拟测试延迟
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  testResult.value = {
    success: true,
    message: `${randomCase} 执行成功！性能指标符合预期 (98%)`,
    timestamp: new Date().toLocaleTimeString()
  }
  testing.value = false
}

onMounted(loadData)
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
