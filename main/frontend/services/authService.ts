export interface User {
  id: number
  nickname: string
  role: string
  totalScore: number
  createdAt: string
}

export interface LoginResponse {
  user: User
  token: string
}

import request from './request'

export const authService = {
  async studentLogin(nickname: string): Promise<LoginResponse> {
    return request.post<LoginResponse, LoginResponse>('/auth/login/student', { nickname })
  },

  async adminLogin(username: string, password: string): Promise<LoginResponse> {
    return request.post<LoginResponse, LoginResponse>('/auth/login/admin', { username, password })
  }
}
