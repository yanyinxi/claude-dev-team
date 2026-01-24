<template>
  <div class="min-h-screen bg-slate-900 text-white p-8 font-sans">
    <!-- Header -->
    <div class="max-w-7xl mx-auto mb-10 flex justify-between items-end">
      <div>
        <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Claude Dev Team v3.0
        </h1>
        <p class="text-slate-400 mt-2 text-lg">LLM-Driven Intelligent Collaboration Monitor</p>
      </div>
      <div class="flex items-center gap-4">
        <div class="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700 flex items-center gap-2">
          <div class="w-2 h-2 rounded-full" :class="health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'"></div>
          <span class="text-sm font-medium">{{ health?.status === 'healthy' ? 'System Online' : 'System Degraded' }}</span>
        </div>
        <button 
          @click="loadData" 
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          :disabled="loading"
        >
          <span v-if="loading" class="animate-spin">⚡</span>
          <span>Refresh</span>
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
            <span class="text-2xl">📊</span> Performance Metrics (Target: 95%+)
          </h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="metric in overview?.metrics" :key="metric.name" 
                 class="bg-slate-900/50 p-4 rounded-xl border border-slate-700/50">
              <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">{{ metric.name }}</div>
              <div class="text-2xl font-bold" :class="metric.status === 'pass' ? 'text-green-400' : 'text-yellow-400'">
                {{ metric.value }}
              </div>
              <div class="text-xs text-slate-500 mt-1">Target: {{ metric.target }}</div>
            </div>
          </div>
        </div>

        <!-- Intelligent Agents -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <span class="text-2xl">🤖</span> Intelligent Agents ({{ agents.length }})
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="agent in agents" :key="agent.name" 
                 class="group p-4 bg-slate-900/50 rounded-xl border border-slate-700/50 hover:border-blue-500/50 transition-all cursor-default">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-medium text-blue-300 group-hover:text-blue-200 transition-colors">{{ formatName(agent.name) }}</h3>
                <span class="text-xs px-2 py-1 bg-slate-800 rounded text-slate-400 border border-slate-700">{{ agent.type }}</span>
              </div>
              <p class="text-sm text-slate-400 line-clamp-2">{{ agent.description }}</p>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Skills & System -->
      <div class="space-y-8">
        
        <!-- Active Skills -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <span class="text-2xl">⚡</span> Active Skills
          </h2>
          <div class="space-y-3">
            <div v-for="skill in skills" :key="skill.name" 
                 class="p-3 bg-slate-900/50 rounded-xl border border-slate-700/50 flex flex-col gap-2">
              <div class="flex justify-between items-center">
                <span class="font-medium text-purple-300">{{ skill.name }}</span>
                <span class="text-xs text-slate-500">{{ skill.tools.length }} tools</span>
              </div>
              <p class="text-xs text-slate-400 line-clamp-2">{{ skill.description }}</p>
            </div>
          </div>
        </div>

        <!-- System Status -->
        <div class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 backdrop-blur-sm">
          <h2 class="text-xl font-semibold mb-4">System Status</h2>
          <div class="space-y-4">
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">Version</span>
              <span class="font-mono text-sm">{{ overview?.version }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">Mode</span>
              <span class="text-blue-400 text-sm">{{ overview?.mode }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-700/50">
              <span class="text-slate-400">Last Update</span>
              <span class="text-sm">{{ overview?.last_update }}</span>
            </div>
            <div class="mt-4">
              <div class="text-xs text-slate-500 mb-2">Health Checks</div>
              <div class="grid grid-cols-2 gap-2">
                <div v-for="(ok, check) in health?.checks" :key="check" 
                     class="flex items-center gap-2 text-xs">
                  <span :class="ok ? 'text-green-500' : 'text-red-500'">●</span>
                  <span class="text-slate-300">{{ formatName(check) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as api from '@/services/monitor'

const loading = ref(false)
const overview = ref<api.SystemOverview>()
const agents = ref<api.AgentData[]>([])
const skills = ref<api.SkillData[]>([])
const health = ref<api.HealthCheck>()

const formatName = (name: string) => {
  return name.split(/[-_]/).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
}

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

onMounted(loadData)
</script>
