<!-- =====================================================
智能诊断中心组件
=====================================================
功能：展示 AI 诊断结果，提供一键修复功能
位置：置顶显示
===================================================== -->

<script setup lang="ts">
import { computed } from 'vue'
import { useMonitorStore } from '@/stores/monitorStore'
import { fixIssue } from '@/services/monitor'

// ==================== 状态管理 ====================

const monitorStore = useMonitorStore()

// ==================== 计算属性 ====================

/**
 * 按严重程度分组的问题
 */
const issuesBySeverity = computed(() => {
  return monitorStore.diagnosisIssuesBySeverity
})

/**
 * 下次诊断倒计时
 */
const nextDiagnosisCountdown = computed(() => {
  if (!monitorStore.diagnosis) return ''

  const now = Date.now()
  const next = new Date(monitorStore.diagnosis.next_diagnosis_time).getTime()
  const diff = next - now
  const minutes = Math.floor(diff / 60000)

  return minutes > 0 ? `${minutes}分钟后` : '即将开始'
})

// ==================== 方法 ====================

/**
 * 一键修复问题
 */
async function handleFix(issueId: string) {
  try {
    await fixIssue(issueId)
    monitorStore.removeFixedIssue(issueId)
    alert('修复成功！')
  } catch (error) {
    alert('修复失败: ' + (error as Error).message)
  }
}

/**
 * 获取严重程度图标
 */
function getSeverityIcon(severity: string) {
  const icons = {
    Critical: '🔴',
    Important: '🟡',
    Suggestion: '🟢'
  }
  return icons[severity as keyof typeof icons] || '⚪'
}
</script>

<template>
  <div class="diagnosis-container">
    <div class="diagnosis-header">
      <h2 class="diagnosis-title">🤖 智能诊断中心</h2>
      <div v-if="monitorStore.diagnosis" class="diagnosis-info">
        <span>上次诊断: {{ new Date(monitorStore.diagnosis.last_diagnosis_time).toLocaleString() }}</span>
        <span class="separator">|</span>
        <span>下次诊断: {{ nextDiagnosisCountdown }}</span>
      </div>
    </div>

    <div v-if="monitorStore.loading.diagnosis" class="loading">
      加载中...
    </div>

    <div v-else-if="!monitorStore.diagnosis" class="empty">
      暂无诊断数据
    </div>

    <div v-else class="diagnosis-content">
      <!-- Critical 问题 -->
      <div v-if="issuesBySeverity.Critical.length > 0" class="severity-group">
        <h3 class="severity-title">
          {{ getSeverityIcon('Critical') }} Critical ({{ issuesBySeverity.Critical.length }})
        </h3>
        <div class="issue-list">
          <div
            v-for="issue in issuesBySeverity.Critical"
            :key="issue.id"
            class="issue-item critical"
          >
            <div class="issue-header">
              <span class="issue-title">{{ issue.title }}</span>
              <span class="issue-category">{{ issue.category }}</span>
            </div>
            <div class="issue-description">{{ issue.description }}</div>
            <div v-if="issue.location" class="issue-location">
              📍 {{ issue.location }}
            </div>
            <div v-if="issue.suggestion" class="issue-suggestion">
              💡 {{ issue.suggestion }}
            </div>
            <div class="issue-actions">
              <button
                v-if="issue.auto_fixable"
                class="fix-btn"
                @click="handleFix(issue.id)"
              >
                一键修复
              </button>
              <button class="ignore-btn">忽略</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Important 问题 -->
      <div v-if="issuesBySeverity.Important.length > 0" class="severity-group">
        <h3 class="severity-title">
          {{ getSeverityIcon('Important') }} Important ({{ issuesBySeverity.Important.length }})
        </h3>
      </div>

      <!-- Suggestion 问题 -->
      <div v-if="issuesBySeverity.Suggestion.length > 0" class="severity-group">
        <h3 class="severity-title">
          {{ getSeverityIcon('Suggestion') }} Suggestion ({{ issuesBySeverity.Suggestion.length }})
        </h3>
      </div>
    </div>
  </div>
</template>

<style scoped>
.diagnosis-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ff6b6b;
}

.diagnosis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.diagnosis-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.diagnosis-info {
  font-size: 14px;
  color: #666;
}

.separator {
  margin: 0 10px;
}

.loading,
.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.severity-group {
  margin-bottom: 20px;
}

.severity-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.issue-item {
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid;
}

.issue-item.critical {
  background: #fff5f5;
  border-left-color: #ff6b6b;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.issue-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.issue-category {
  padding: 4px 12px;
  background: #f1f3f5;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.issue-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.issue-location,
.issue-suggestion {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
}

.issue-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.fix-btn,
.ignore-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.fix-btn {
  background: #667eea;
  color: white;
}

.fix-btn:hover {
  background: #5568d3;
}

.ignore-btn {
  background: #f1f3f5;
  color: #666;
}

.ignore-btn:hover {
  background: #e9ecef;
}
</style>
