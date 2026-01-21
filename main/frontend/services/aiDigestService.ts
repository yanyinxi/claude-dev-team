/**
 * AI 日报 API 服务
 *
 * 功能：
 * - 获取最新日报
 * - 获取指定日期日报
 * - 获取日报列表
 */

import axios from 'axios'

// API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// AI 日报摘要项
export interface AiDigestSummaryItem {
  title: string
  url: string
  description: string
}

// AI 日报响应
export interface AiDigestResponse {
  id: number
  date: string
  title: string
  summary: AiDigestSummaryItem[]
  content: string // JSON string, parse with JSON.parse()
  total_items: number
  created_at: string
}

// AI 日报列表项
export interface AiDigestListItem {
  id: number
  date: string
  title: string
  total_items: number
  created_at: string
}

/**
 * 获取最新日报
 */
export async function getLatestDigest(): Promise<AiDigestResponse> {
  const response = await axios.get(`${API_BASE_URL}/api/v1/ai-digest/latest`)
  return response.data
}

/**
 * 获取指定日期的日报
 *
 * @param date - 日期（格式：YYYY-MM-DD）
 */
export async function getDigestByDate(date: string): Promise<AiDigestResponse> {
  const response = await axios.get(`${API_BASE_URL}/api/v1/ai-digest/${date}`)
  return response.data
}

/**
 * 获取日报列表
 *
 * @param skip - 跳过数量
 * @param limit - 返回数量
 */
export async function getDigestList(
  skip: number = 0,
  limit: number = 10
): Promise<AiDigestListItem[]> {
  const response = await axios.get(`${API_BASE_URL}/api/v1/ai-digest`, {
    params: { skip, limit }
  })
  return response.data
}

export default {
  getLatestDigest,
  getDigestByDate,
  getDigestList
}
