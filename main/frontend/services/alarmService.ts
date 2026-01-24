import request from './request'
import type { AlarmStatus, AlarmValidation, AlarmRule } from '@/stores/alarmStore'

// =====================================================
// 学习闹钟 API 服务
// 功能：封装闹钟相关的 HTTP 请求
// =====================================================

export interface AlarmRuleCreate {
  rule_type: 'global' | 'personal'
  student_nickname?: string
  study_duration: number
  rest_duration: number
}

export interface AlarmRuleUpdate {
  study_duration?: number
  rest_duration?: number
  is_active?: boolean
}

/**
 * 获取当前学习状态
 */
export async function getAlarmStatus(): Promise<AlarmStatus> {
  return request.get('/alarm/status')
}

/**
 * 开始学习
 */
export async function startAlarm(): Promise<AlarmStatus> {
  return request.post('/alarm/start')
}

/**
 * 验证是否可以操作
 */
export async function validateAlarm(): Promise<AlarmValidation> {
  return request.get('/alarm/validate')
}

/**
 * 获取所有规则（管理员）
 */
export async function getAllRules(): Promise<AlarmRule[]> {
  return request.get('/alarm/rules')
}

/**
 * 创建规则（管理员）
 */
export async function createRule(data: AlarmRuleCreate): Promise<AlarmRule> {
  return request.post('/alarm/rules', data)
}

/**
 * 更新规则（管理员）
 */
export async function updateRule(id: number, data: AlarmRuleUpdate): Promise<AlarmRule> {
  return request.put(`/alarm/rules/${id}`, data)
}

/**
 * 删除规则（管理员）
 */
export async function deleteRule(id: number): Promise<void> {
  return request.delete(`/alarm/rules/${id}`)
}

/**
 * 启用/禁用规则（管理员）
 */
export async function toggleRule(id: number): Promise<AlarmRule> {
  return request.patch(`/alarm/rules/${id}/toggle`)
}
