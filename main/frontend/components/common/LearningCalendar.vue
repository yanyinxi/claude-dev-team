<script setup lang="ts">
import { ref, computed } from 'vue'
import Button from '@/components/common/Button.vue'

// =====================================================
// 学习日历组件
// 功能：展示每日学习打卡记录，支持进度追踪
// =====================================================

interface Props {
  // 学习记录：日期字符串数组
  studyDates?: string[]
  // 每日完成题数
  dailyProgress?: Record<string, number>
}

const props = withDefaults(defineProps<Props>(), {
  studyDates: () => [],
  dailyProgress: () => ({})
})

// 当前显示的月份
const currentDate = ref(new Date())
const selectedDate = ref<string | null>(null)

// 计算当前月份信息
const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())

// 月份名称
const monthNames = [
  '一月', '二月', '三月', '四月', '五月', '六月',
  '七月', '八月', '九月', '十月', '十一月', '十二月'
]

// 生成当月日历数据
const calendarDays = computed(() => {
  const days = []
  const year = currentYear.value
  const month = currentMonth.value

  // 月第一天
  const firstDay = new Date(year, month, 1)
  // 月最后一天
  const lastDay = new Date(year, month + 1, 0)

  // 月第一天是星期几 (0 = 周日)
  const firstDayOfWeek = firstDay.getDay()

  // 添加空白天数
  for (let i = 0; i < firstDayOfWeek; i++) {
    days.push({ date: null, day: '' })
  }

  // 添加当月所有天数
  for (let day = 1; day <= lastDay.getDate(); day++) {
    const dateStr = formatDate(year, month + 1, day)
    const studyCount = props.dailyProgress[dateStr] || 0
    const isStudied = props.studyDates.includes(dateStr)
    const isToday = isTodayFn(year, month + 1, day)

    days.push({
      date: dateStr,
      day,
      isStudied,
      studyCount,
      isToday
    })
  }

  return days
})

// 格式化日期为 YYYY-MM-DD
function formatDate(year: number, month: number, day: number): string {
  const m = month.toString().padStart(2, '0')
  const d = day.toString().padStart(2, '0')
  return `${year}-${m}-${d}`
}

// 判断是否是今天
function isTodayFn(year: number, month: number, day: number): boolean {
  const today = new Date()
  return today.getFullYear() === year &&
         today.getMonth() + 1 === month &&
         today.getDate() === day
}

// 上个月
function prevMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

// 下个月
function nextMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

// 跳转到今天
function goToToday() {
  currentDate.value = new Date()
}

// 统计信息
const stats = computed(() => {
  const totalDays = props.studyDates.length
  const consecutiveDays = calculateConsecutiveDays()

  return {
    totalDays,
    consecutiveDays,
    completionRate: Math.round((totalDays / 30) * 100)
  }
})

// 计算连续学习天数
function calculateConsecutiveDays(): number {
  if (props.studyDates.length === 0) return 0

  const sortedDates = [...props.studyDates].sort().reverse()
  let consecutive = 1
  const today = new Date()
  const todayStr = formatDate(today.getFullYear(), today.getMonth() + 1, today.getDate())

  // 检查今天是否学习
  if (!props.studyDates.includes(todayStr)) {
    consecutive = 0
  }

  // 计算连续天数
  for (let i = 0; i < sortedDates.length - 1; i++) {
    const current = new Date(sortedDates[i])
    const next = new Date(sortedDates[i + 1])
    const diffDays = Math.floor((current.getTime() - next.getTime()) / (1000 * 60 * 60 * 24))

    if (diffDays === 1) {
      consecutive++
    } else {
      break
    }
  }

  return consecutive
}

// 选择日期
function selectDate(date: string | null) {
  selectedDate.value = date
}
</script>

<template>
  <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-4 shadow-2xl">
    <!-- 头部：月份导航 ---->
    <div class="flex items-center justify-between mb-4">
      <Button
        variant="secondary"
        class="w-8 h-8 rounded-full p-0 flex items-center justify-center text-sm"
        @click="prevMonth"
      >
        ◀
      </Button>

      <div class="text-center">
        <h3 class="text-lg font-black text-gray-800">
          {{ currentYear }} 年 {{ monthNames[currentMonth] }}
        </h3>
        <button
          class="text-xs text-blue-500 hover:text-blue-700 transition font-medium"
          @click="goToToday"
        >
          回到今天
        </button>
      </div>

      <Button
        variant="secondary"
        class="w-8 h-8 rounded-full p-0 flex items-center justify-center text-sm"
        @click="nextMonth"
      >
        ▶
      </Button>
    </div>

    <!-- 统计信息 ---->
    <div class="grid grid-cols-3 gap-2 mb-4">
      <div class="bg-gradient-to-br from-blue-400 to-blue-500 rounded-xl p-3 text-center">
        <div class="text-2xl font-black text-white">{{ stats.totalDays }}</div>
        <div class="text-xs text-white/80">总学习天数</div>
      </div>
      <div class="bg-gradient-to-br from-green-400 to-green-500 rounded-xl p-3 text-center">
        <div class="text-2xl font-black text-white">{{ stats.consecutiveDays }}</div>
        <div class="text-xs text-white/80">连续天数</div>
      </div>
      <div class="bg-gradient-to-br from-purple-400 to-purple-500 rounded-xl p-3 text-center">
        <div class="text-2xl font-black text-white">{{ stats.completionRate }}%</div>
        <div class="text-xs text-white/80">本月完成</div>
      </div>
    </div>

    <!-- 星期标题 ---->
    <div class="grid grid-cols-7 gap-1 mb-1">
      <div
        v-for="day in ['日', '一', '二', '三', '四', '五', '六']"
        :key="day"
        class="text-center text-xs font-bold text-gray-500 py-1"
      >
        {{ day }}
      </div>
    </div>

    <!-- 日历格子 ---->
    <div class="grid grid-cols-7 gap-1">
      <div
        v-for="(item, index) in calendarDays"
        :key="index"
        :class="[
          'aspect-square flex flex-col items-center justify-center rounded-lg text-xs cursor-pointer transition-all',
          !item.date ? 'invisible' : '',
          item.date && item.isToday ? 'ring-2 ring-blue-400' : '',
          item.date && selectedDate === item.date ? 'bg-blue-100' : '',
          item.date && item.isStudied ? 'bg-green-100 hover:bg-green-200' : 'hover:bg-gray-100'
        ]"
        @click="selectDate(item.date)"
      >
        <span class="font-bold" :class="item.isStudied ? 'text-green-600' : 'text-gray-700'">
          {{ item.day }}
        </span>
        <!-- 学习标记 ---->
        <span
          v-if="item.isStudied && item.date"
          class="text-xs mt-0.5"
        >
          {{ item.studyCount > 0 ? '📚' : '✓' }}
        </span>
      </div>
    </div>

    <!-- 图例 ---->
    <div class="flex items-center justify-center gap-3 mt-3 text-xs text-gray-500">
      <div class="flex items-center gap-1">
        <span class="w-3 h-3 bg-green-100 rounded"></span>
        <span>已学习</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="w-3 h-3 ring-2 ring-blue-400 rounded"></span>
        <span>今天</span>
      </div>
    </div>
  </div>
</template>
