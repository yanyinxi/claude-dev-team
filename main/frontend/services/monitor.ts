/**
 * AlphaZero 监控系统 - API 服务
 * 
 * 提供与后端监控 API 的交互接口
 */

import request from './request'

// 类型定义
export interface SystemStats {
  agents_count: number
  hooks_count: number
  rules_count: number
  experience_count: number
  avg_reward: number
  recent_24h_count: number
  by_agent: Record<string, number>
  by_keyword: Record<string, number>
  healthy: boolean
}

export interface AgentInfo {
  name: string
  description: string
  tools: string[]
  file_size: number
  updated: string
}

export interface RuleInfo {
  name: string
  updated: string
  insights_count: number
  file_size: number
}

export interface ExperienceRecord {
  agent: string
  reward: number
  timestamp: string
  strategy_keyword: string
  result_preview: string
}

export interface ExperiencePool {
  total: number
  records: ExperienceRecord[]
  avg_reward: number
}

export interface HookConfig {
  matcher: string
  hooks: {
    type: string
    command: string
  }[]
}

export interface HealthCheck {
  status: 'healthy' | 'degraded'
  checks: Record<string, boolean>
  timestamp: string
}

const API_BASE = ''

/**
 * 获取系统运行状态统计
 */
export async function getSystemStats(): Promise<SystemStats> {
  return await request.get('stats')
}

/**
 * 获取所有 Agent 信息
 */
export async function getAgentsInfo(): Promise<AgentInfo[]> {
  return await request.get('agents')
}

/**
 * 获取所有策略规则信息
 */
export async function getRulesInfo(): Promise<RuleInfo[]> {
  return await request.get('rules')
}

/**
 * 获取经验池数据
 */
export async function getExperiencePool(limit: number = 50): Promise<ExperiencePool> {
  return await request.get('experience', {
    params: { limit }
  })
}

/**
 * 获取 Hooks 配置状态
 */
export async function getHooksStatus(): Promise<Record<string, HookConfig[]>> {
  return await request.get('hooks')
}

/**
 * 系统健康检查
 */
export async function healthCheck(): Promise<HealthCheck> {
  return await request.get('health')
}

/**
 * 刷新监控数据（同时获取所有数据）
 */
export async function refreshAllData() {
  const [stats, agents, rules, hooks, health] = await Promise.all([
    getSystemStats(),
    getAgentsInfo(),
    getRulesInfo(),
    getHooksStatus(),
    healthCheck()
  ])
  
  return {
    stats,
    agents,
    rules,
    hooks,
    health
  }
}
