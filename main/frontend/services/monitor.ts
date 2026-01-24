import request from './request'

export interface PerformanceMetric {
  name: string
  value: string
  target: string
  status: 'pass' | 'fail' | 'warning'
}

export interface SystemOverview {
  version: string
  mode: string
  status: string
  last_update: string
  metrics: PerformanceMetric[]
}

export interface AgentData {
  name: string
  description: string
  type: string
  updated: string
}

export interface SkillData {
  name: string
  description: string
  tools: string[]
}

export interface HealthCheck {
  status: 'healthy' | 'degraded'
  checks: Record<string, boolean>
  timestamp: string
  version: string
}

export async function getSystemOverview(): Promise<SystemOverview> {
  return await request.get('monitor/overview')
}

export async function getAgents(): Promise<AgentData[]> {
  return await request.get('monitor/agents')
}

export async function getSkills(): Promise<SkillData[]> {
  return await request.get('monitor/skills')
}

export async function checkHealth(): Promise<HealthCheck> {
  return await request.get('monitor/health')
}
