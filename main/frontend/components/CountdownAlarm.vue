<script setup lang="ts">
/**
 * CountdownAlarm.vue — 通用倒计时闹钟组件
 *
 * 功能：
 *   - 用户自定义输入时长（分钟 + 秒）
 *   - 开始 / 暂停 / 重置控制
 *   - 圆形 SVG 进度条可视化
 *   - 时间归零时：
 *       1. 桌面通知（Web Notifications API）
 *       2. 页面内完成弹窗
 *       3. Web Audio API beep 提示音
 */

import { ref, computed, watch } from 'vue'
import { useCountdownTimer } from '@/composables/useCountdownTimer'
import { useNotification } from '@/composables/useNotification'

// ---- 圆形进度条参数 ----
const RADIUS = 80          // 圆的半径（px）
const STROKE_WIDTH = 10    // 描边宽度（px）
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

// ---- 通知权限 ----
const { hasPermission, requestPermission, triggerAll } = useNotification()

// ---- 完成弹窗状态 ----
const showCompletionModal = ref(false)

// ---- 倒计时逻辑 ----
const { duration, remaining, isRunning, isPaused, progress, formattedTime, start, pause, resume, reset } =
  useCountdownTimer({
    onComplete() {
      // 归零时：播放 beep + 桌面通知 + 页面内弹窗
      triggerAll('倒计时结束', '您设定的倒计时已经结束！')
      showCompletionModal.value = true
    }
  })

// ---- 用户输入（未运行时可编辑） ----
const inputMinutes = ref<number>(5)
const inputSeconds = ref<number>(0)

// 验证输入范围
function clampMinutes(val: number): number {
  return Math.max(0, Math.min(99, Math.floor(val)))
}
function clampSeconds(val: number): number {
  return Math.max(0, Math.min(59, Math.floor(val)))
}

function onMinutesInput(e: Event) {
  const v = parseInt((e.target as HTMLInputElement).value) || 0
  inputMinutes.value = clampMinutes(v)
}
function onSecondsInput(e: Event) {
  const v = parseInt((e.target as HTMLInputElement).value) || 0
  inputSeconds.value = clampSeconds(v)
}

/** 用户输入换算为秒 */
const totalInputSeconds = computed(() => inputMinutes.value * 60 + inputSeconds.value)

// ---- SVG 进度条 ----
/**
 * strokeDashoffset：进度越大，偏移越小（越多轮廓被描边填满）
 * 初始值 = CIRCUMFERENCE（全部偏移 = 空圆）
 * 结束值 = 0（无偏移 = 满圆）
 */
const strokeDashoffset = computed(() => {
  return CIRCUMFERENCE * (1 - progress.value / 100)
})

// 进度条颜色：最后 10% 变红
const progressColor = computed(() => {
  if (progress.value >= 90) return '#ef4444'   // red-500
  if (progress.value >= 70) return '#f97316'   // orange-500
  return '#6366f1'                              // indigo-500
})

// ---- 控制按钮 ----

async function handleStart() {
  // 首次开始时请求通知权限
  if (hasPermission.value === 'default') {
    await requestPermission()
  }
  start(totalInputSeconds.value)
}

function handlePause() {
  if (isRunning.value) {
    pause()
  } else if (isPaused.value) {
    resume()
  }
}

function handleReset() {
  reset()
  showCompletionModal.value = false
  // 重置后 remaining 恢复为 duration，同步更新 input 框
  const mins = Math.floor(duration.value / 60)
  const secs = duration.value % 60
  inputMinutes.value = mins
  inputSeconds.value = secs
}

function closeModal() {
  showCompletionModal.value = false
}

// 运行中时将 formattedTime 反映到 input 框（可选展示用，不影响编辑逻辑）
// 为避免干扰，只在 idle 状态才同步 input
watch(
  () => isRunning.value || isPaused.value,
  (active) => {
    if (!active) {
      inputMinutes.value = Math.floor(duration.value / 60)
      inputSeconds.value = duration.value % 60
    }
  }
)

// 格式化剩余时间供弹窗显示
const displayTime = computed(() => {
  if (isRunning.value || isPaused.value) return formattedTime.value
  // idle 时显示设定值
  const m = String(inputMinutes.value).padStart(2, '0')
  const s = String(inputSeconds.value).padStart(2, '0')
  return `${m}:${s}`
})

// 是否允许点击"开始"
const canStart = computed(() => totalInputSeconds.value > 0)
</script>

<template>
  <div class="countdown-alarm">
    <!-- 标题栏 -->
    <div class="alarm-header">
      <span class="alarm-title-icon">⏱</span>
      <h2 class="alarm-title">倒计时闹钟</h2>
    </div>

    <!-- 通知权限提示 -->
    <div v-if="hasPermission === 'default'" class="permission-banner">
      <span class="permission-icon">🔔</span>
      <span class="permission-text">开启浏览器通知，倒计时结束时会提醒您</span>
      <button class="permission-btn" @click="requestPermission">允许通知</button>
    </div>
    <div v-if="hasPermission === 'denied'" class="permission-banner permission-banner--denied">
      <span class="permission-icon">🔕</span>
      <span class="permission-text">通知权限已被拒绝，结束时将只显示页面弹窗和声音提示</span>
    </div>

    <!-- 圆形进度条 + 时间显示 -->
    <div class="ring-container">
      <svg
        :width="RADIUS * 2 + STROKE_WIDTH * 2"
        :height="RADIUS * 2 + STROKE_WIDTH * 2"
        class="ring-svg"
      >
        <!-- 背景圆环 -->
        <circle
          :cx="RADIUS + STROKE_WIDTH"
          :cy="RADIUS + STROKE_WIDTH"
          :r="RADIUS"
          fill="none"
          stroke="#e5e7eb"
          :stroke-width="STROKE_WIDTH"
        />
        <!-- 进度圆环，顺时针从顶部开始 -->
        <circle
          :cx="RADIUS + STROKE_WIDTH"
          :cy="RADIUS + STROKE_WIDTH"
          :r="RADIUS"
          fill="none"
          :stroke="progressColor"
          :stroke-width="STROKE_WIDTH"
          stroke-linecap="round"
          :stroke-dasharray="CIRCUMFERENCE"
          :stroke-dashoffset="strokeDashoffset"
          transform="rotate(-90deg)"
          style="transform-origin: center; transform: rotate(-90deg); transition: stroke-dashoffset 0.8s ease, stroke 0.5s ease;"
        />
      </svg>

      <!-- 中心时间文字 -->
      <div class="ring-center">
        <div class="ring-time" :class="{ 'ring-time--warning': progress >= 90 }">
          {{ displayTime }}
        </div>
        <div class="ring-status">
          <span v-if="isRunning" class="status-dot status-dot--running"></span>
          <span v-else-if="isPaused" class="status-dot status-dot--paused"></span>
          <span v-else class="status-dot status-dot--idle"></span>
          <span class="status-label">
            {{ isRunning ? '运行中' : isPaused ? '已暂停' : '未开始' }}
          </span>
        </div>
      </div>
    </div>

    <!-- 时间输入区（仅在未运行时可编辑） -->
    <div class="input-section">
      <div class="input-group">
        <label class="input-label">分钟</label>
        <input
          type="number"
          class="time-input"
          :value="inputMinutes"
          :disabled="isRunning || isPaused"
          min="0"
          max="99"
          @input="onMinutesInput"
        />
      </div>
      <div class="input-separator">:</div>
      <div class="input-group">
        <label class="input-label">秒</label>
        <input
          type="number"
          class="time-input"
          :value="inputSeconds"
          :disabled="isRunning || isPaused"
          min="0"
          max="59"
          @input="onSecondsInput"
        />
      </div>
    </div>

    <!-- 快速预设 -->
    <div v-if="!isRunning && !isPaused" class="presets">
      <button class="preset-btn" @click="() => { inputMinutes = 1; inputSeconds = 0 }">1分钟</button>
      <button class="preset-btn" @click="() => { inputMinutes = 5; inputSeconds = 0 }">5分钟</button>
      <button class="preset-btn" @click="() => { inputMinutes = 10; inputSeconds = 0 }">10分钟</button>
      <button class="preset-btn" @click="() => { inputMinutes = 25; inputSeconds = 0 }">25分钟</button>
    </div>

    <!-- 控制按钮 -->
    <div class="controls">
      <!-- 开始按钮（仅 idle 时显示） -->
      <button
        v-if="!isRunning && !isPaused"
        class="ctrl-btn ctrl-btn--start"
        :disabled="!canStart"
        @click="handleStart"
      >
        <span class="ctrl-icon">▶</span>
        开始
      </button>

      <!-- 暂停 / 继续（运行或暂停时显示） -->
      <button
        v-if="isRunning || isPaused"
        class="ctrl-btn ctrl-btn--pause"
        @click="handlePause"
      >
        <span class="ctrl-icon">{{ isRunning ? '⏸' : '▶' }}</span>
        {{ isRunning ? '暂停' : '继续' }}
      </button>

      <!-- 重置按钮（非 idle 时显示） -->
      <button
        v-if="isRunning || isPaused"
        class="ctrl-btn ctrl-btn--reset"
        @click="handleReset"
      >
        <span class="ctrl-icon">↺</span>
        重置
      </button>
    </div>

    <!-- 倒计时完成弹窗 -->
    <Transition name="modal-fade">
      <div v-if="showCompletionModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card">
          <div class="modal-icon">🎉</div>
          <h3 class="modal-title">时间到！</h3>
          <p class="modal-body">您设定的倒计时已经结束，休息一下吧。</p>
          <div class="modal-actions">
            <button class="modal-btn modal-btn--primary" @click="closeModal">好的</button>
            <button class="modal-btn modal-btn--secondary" @click="handleReset">重新设置</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* =====================================================
   CountdownAlarm 样式
   风格：与 LearningZone 整体白色卡片保持一致
===================================================== */

.countdown-alarm {
  background: #ffffff;
  border-radius: 20px;
  padding: 28px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  position: relative;
}

/* 标题 */
.alarm-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  justify-content: center;
}

.alarm-title-icon {
  font-size: 24px;
}

.alarm-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

/* 通知权限横幅 */
.permission-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 16px;
  font-size: 13px;
  color: #1e40af;
  flex-wrap: wrap;
}

.permission-banner--denied {
  background: #fef2f2;
  border-color: #fecaca;
  color: #991b1b;
}

.permission-icon {
  flex-shrink: 0;
  font-size: 16px;
}

.permission-text {
  flex: 1;
  min-width: 0;
}

.permission-btn {
  flex-shrink: 0;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.permission-btn:hover {
  background: #1d4ed8;
}

/* 圆形进度条 */
.ring-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 8px auto 20px;
  width: fit-content;
}

.ring-svg {
  display: block;
  overflow: visible;
  filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.2));
}

.ring-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.ring-time {
  font-size: 36px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #1e293b;
  letter-spacing: 2px;
  transition: color 0.4s;
}

.ring-time--warning {
  color: #ef4444;
  animation: warning-pulse 1s ease-in-out infinite;
}

@keyframes warning-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.ring-status {
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot--running {
  background: #22c55e;
  animation: blink 1s ease-in-out infinite;
}

.status-dot--paused {
  background: #f59e0b;
}

.status-dot--idle {
  background: #94a3b8;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.status-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

/* 时间输入 */
.input-section {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 8px;
  margin-bottom: 14px;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.input-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.time-input {
  width: 72px;
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #1e293b;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 4px;
  outline: none;
  transition: border-color 0.2s;
  background: #f8fafc;
  /* 隐藏数字 spinner */
  -moz-appearance: textfield;
}

.time-input::-webkit-outer-spin-button,
.time-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.time-input:focus:not(:disabled) {
  border-color: #6366f1;
  background: #fff;
}

.time-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f1f5f9;
}

.input-separator {
  font-size: 28px;
  font-weight: 700;
  color: #cbd5e1;
  line-height: 1;
  padding-bottom: 6px;
}

/* 快速预设 */
.presets {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.preset-btn {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.preset-btn:hover {
  background: #6366f1;
  color: #fff;
  border-color: #6366f1;
}

/* 控制按钮 */
.controls {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.ctrl-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 28px;
  border-radius: 50px;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.ctrl-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ctrl-btn--start {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}

.ctrl-btn--start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
}

.ctrl-btn--pause {
  background: linear-gradient(135deg, #f59e0b, #f97316);
  color: #fff;
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
}

.ctrl-btn--pause:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
}

.ctrl-btn--reset {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.ctrl-btn--reset:hover {
  background: #e2e8f0;
}

.ctrl-icon {
  font-size: 14px;
  line-height: 1;
}

/* 完成弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-card {
  background: #fff;
  border-radius: 20px;
  padding: 36px 32px;
  text-align: center;
  max-width: 360px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.modal-icon {
  font-size: 56px;
  margin-bottom: 16px;
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%   { transform: scale(0.5); opacity: 0; }
  60%  { transform: scale(1.1); }
  100% { transform: scale(1); opacity: 1; }
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 10px;
}

.modal-body {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 24px;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-btn {
  padding: 10px 24px;
  border-radius: 50px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn--primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}

.modal-btn--primary:hover {
  transform: translateY(-2px);
}

.modal-btn--secondary {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.modal-btn--secondary:hover {
  background: #e2e8f0;
}

/* 弹窗动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 480px) {
  .countdown-alarm {
    padding: 20px 16px;
    border-radius: 16px;
  }

  .ring-time {
    font-size: 28px;
  }

  .ctrl-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>
