/**
 * 抢答模式 API 服务
 */
import request from './request'

export interface SpeedQuizStartRequest {
  difficulty: number
  module: string
  rounds: number
}

export interface Question {
  id: number
  question_text: string
  option_a: string
  option_b: string
  option_c?: string
  option_d?: string
}

export interface SpeedQuizStartResponse {
  battle_id: number
  question: Question
}

export interface SpeedQuizSubmitRequest {
  battle_id: number
  question_id: number
  answer: string
  answer_time: number
}

export interface SpeedQuizSubmitResponse {
  is_correct: boolean
  ai_answer: string
  ai_time: number
  correct_answer: string
  winner: string
  next_question: Question | null
}

export interface SpeedQuizStats {
  total_battles: number
  wins: number
  losses: number
  win_rate: number
  fastest_time: number
  max_streak: number
}

export interface SpeedQuizBattle {
  id: number
  difficulty: number
  module: string
  user_wins: number
  ai_wins: number
  created_at: string
}

export interface SpeedQuizHistory {
  battles: SpeedQuizBattle[]
  total: number
  page: number
  page_size: number
}

/**
 * 开始抢答
 */
export const startSpeedQuiz = (data: SpeedQuizStartRequest): Promise<SpeedQuizStartResponse> => {
  return request.post('/speed-quiz/start', data)
}

/**
 * 提交答案
 */
export const submitSpeedQuizAnswer = (data: SpeedQuizSubmitRequest): Promise<SpeedQuizSubmitResponse> => {
  return request.post('/speed-quiz/submit', data)
}

/**
 * 获取战绩统计
 */
export const getSpeedQuizStats = (): Promise<SpeedQuizStats> => {
  return request.get('/speed-quiz/stats')
}

/**
 * 获取历史记录
 */
export const getSpeedQuizHistory = (page: number = 1, pageSize: number = 10): Promise<SpeedQuizHistory> => {
  return request.get('/speed-quiz/history', { params: { page, page_size: pageSize } })
}
