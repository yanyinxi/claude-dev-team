<!-- =====================================================
     Agent 性能监控组件
     =====================================================
     功能：展示所有 Agent 的当前进度和历史性能数据
     职责：
     1. 显示 Agent 名称和功能描述
     2. 实时显示 Agent 工作状态（工作中/已完成/失败/空闲）
     3. 可视化展示当前任务进度（进度条）
     4. 统计历史性能数据（总任务数、成功率、平均耗时）

     数据来源：monitorStore.agentPerformance
     更新方式：页面加载时获取 + 手动刷新
     ===================================================== -->

<script setup lang="ts">
import { computed } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'

const monitorStore = useMonitorStore()

// ==================== Agent 描述映射表 ====================
// 为每个 Agent 提供功能说明，帮助用户理解各个 Agent 的职责
const agentDescriptions: Record<string, string> = {
  'product-manager': '需求分析和 PRD 生成，负责分析用户需求、编写产品需求文档',
  'tech-lead': '架构设计和技术选型，负责系统架构设计、技术方案评审',
  'frontend-developer': '前端开发，负责实现用户界面和交互逻辑',
  'backend-developer': '后端开发，负责实现 API 接口、业务逻辑和数据库操作',
  'test': '测试工程师，负责测试规划、编写测试用例、执行测试',
  'code-reviewer': '代码审查，负责审查代码质量、安全性和最佳实践',
  'orchestrator': '主协调器，负责协调多个 Agent 的工作流程',
  'evolver': '自进化引擎，负责从执行结果中学习并更新系统配置',
  'progress-viewer': '进度查询，负责查看任务执行进度和状态',
  'strategy-selector': 'AlphaZero 策略选择器，负责选择最优执行策略',
  'self-play-trainer': 'AlphaZero 自博弈训练器，负责生成并评估多种策略变体'
}

// ==================== 计算属性 ====================

/**
 * Agent 列表
 * 从 monitorStore 获取所有 Agent 的性能数据
 */
const agents = computed(() => monitorStore.agentPerformance)

// ==================== 方法 ====================

/**
 * 获取 Agent 描述
 * @param agentName Agent 名称
 * @returns Agent 功能描述
 */
function getAgentDescription(agentName: string): string {
  return agentDescriptions[agentName] || '暂无描述'
}

/**
 * 获取进度条颜色
 * 根据进度百分比返回不同颜色：
 * - 80% 以上：绿色（表示进展顺利）
 * - 50-80%：橙色（表示进行中）
 * - 50% 以下：红色（表示进度较慢）
 *
 * @param progress 进度百分比（0-100）
 * @returns 颜色值（十六进制）
 */
function getProgressColor(progress: number) {
  if (progress >= 80) return '#67C23A'  // 绿色
  if (progress >= 50) return '#E6A23C'  // 橙色
  return '#F56C6C'                      // 红色
}

/**
 * 获取状态徽章
 * 根据 Agent 状态返回对应的徽章文本和颜色
 *
 * @param status Agent 状态
 * @returns 徽章配置（文本 + 颜色）
 */
function getStatusBadge(status: string) {
  const badges = {
    working: { text: '工作中', color: '#67C23A' },      // 绿色
    completed: { text: '已完成', color: '#409EFF' },    // 蓝色
    failed: { text: '失败', color: '#F56C6C' },         // 红色
    idle: { text: '空闲', color: '#909399' }            // 灰色
  }
  return badges[status as keyof typeof badges] || badges.idle
}

/**
 * 格式化时长
 * 将秒数转换为分钟显示
 *
 * @param seconds 秒数
 * @returns 格式化后的时长字符串（如 "5分钟"）
 */
function formatDuration(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}
</script>

<template>
  <div class="agent-progress-container">
    <h2 class="progress-title">🤖 Agent 性能监控</h2>

    <!-- 加载状态 -->
    <div v-if="monitorStore.loading.agents" class="loading">
      加载中...
    </div>

    <!-- 空状态 -->
    <div v-else-if="agents.length === 0" class="empty">
      暂无 Agent 数据
    </div>

    <!-- Agent 列表 -->
    <div v-else class="agent-list">
      <div
        v-for="agent in agents"
        :key="agent.name"
        class="agent-item"
      >
        <!-- Agent 头部：名称、描述、状态 -->
        <div class="agent-header">
          <div class="agent-info">
            <span class="agent-name">{{ agent.name }}</span>
            <span class="agent-description">{{ getAgentDescription(agent.name) }}</span>
          </div>
          <span
            class="agent-status"
            :style="{ background: getStatusBadge(agent.status).color }"
          >
            {{ getStatusBadge(agent.status).text }}
          </span>
        </div>

        <!-- 进度条 -->
        <div class="progress-bar-container">
          <div
            class="progress-bar"
            :style="{
              width: agent.current_progress + '%',
              background: getProgressColor(agent.current_progress)
            }"
          ></div>
        </div>

        <!-- 性能统计 -->
        <div class="agent-stats">
          <span>总任务: {{ agent.performance.total_tasks }}</span>
          <span>成功率: {{ (agent.performance.success_rate * 100).toFixed(0) }}%</span>
          <span>平均耗时: {{ formatDuration(agent.performance.avg_duration_seconds) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.agent-progress-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.progress-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.loading,
.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.agent-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.agent-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.agent-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.agent-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.agent-description {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

.agent-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
}

.progress-bar-container {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-bar {
  height: 100%;
  transition: width 0.3s;
}

.agent-stats {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
}
</style>
