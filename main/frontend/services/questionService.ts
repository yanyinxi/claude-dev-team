import request from './request'

interface ApiQuestion {
  id: number
  module: string
  difficulty: number
  question_text: string
  question_image?: string
  option_a: string
  option_b: string
  option_c?: string
  option_d?: string
}

export interface Question {
  id: number
  module: string
  difficulty: number
  questionText: string
  questionImage?: string
  optionA: string
  optionB: string
  optionC?: string
  optionD?: string
}

export interface AnswerResult {
  isCorrect: boolean
  correctAnswer: string
  explanation?: string
  score: number
  streak: number
  newAchievements: any[]
  encouragement: string
}

export interface ProgressData {
  totalQuestions: number
  correctAnswers: number
  accuracy: number
  streak: number
  dailyGoal: number
  completedToday: number
  studyDates?: string[]
  dailyProgress?: Record<string, number>
}

interface ApiStudyRecord {
  date: string
  questions_completed: number
  total_score: number
}

interface ApiStudyRecordsResponse {
  records: ApiStudyRecord[]
  total_days: number
  consecutive_days: number
}

export interface StudyRecord {
  date: string
  questionsCompleted: number
  totalScore: number
}

export interface StudyRecordsResponse {
  records: StudyRecord[]
  totalDays: number
  consecutiveDays: number
}
interface ApiWrongQuestion {
  id: number
  question_id?: number
  questionId?: number
  question_text?: string
  questionText?: string
  question_image?: string
  questionImage?: string
  option_a?: string
  optionA?: string
  option_b?: string
  optionB?: string
  option_c?: string
  optionC?: string
  option_d?: string
  optionD?: string
  correctAnswer: string
  explanation?: string
  module: string
  difficulty: number
  wrongCount: number
  lastWrongAt: string
}

export interface WrongQuestion {
  id: number
  questionId: number
  questionText: string
  questionImage?: string
  optionA: string
  optionB: string
  optionC?: string
  optionD?: string
  correctAnswer: string
  explanation?: string
  module: string
  difficulty: number
  wrongCount: number
  lastWrongAt: string
}

export interface WrongQuestionsResponse {
  items: WrongQuestion[]
  total: number
  page: number
  pageSize: number
}

function mapQuestion(data: ApiQuestion): Question {
  return {
    id: data.id,
    module: data.module,
    difficulty: data.difficulty,
    questionText: data.question_text,
    questionImage: data.question_image,
    optionA: data.option_a,
    optionB: data.option_b,
    optionC: data.option_c,
    optionD: data.option_d
  }
}

function mapWrongQuestion(data: ApiWrongQuestion): WrongQuestion {
  return {
    id: data.id,
    questionId: data.questionId ?? data.question_id ?? data.id,
    questionText: data.questionText ?? data.question_text ?? '',
    questionImage: data.questionImage ?? data.question_image,
    optionA: data.optionA ?? data.option_a ?? '',
    optionB: data.optionB ?? data.option_b ?? '',
    optionC: data.optionC ?? data.option_c,
    optionD: data.optionD ?? data.option_d,
    correctAnswer: data.correctAnswer,
    explanation: data.explanation,
    module: data.module,
    difficulty: data.difficulty,
    wrongCount: data.wrongCount,
    lastWrongAt: data.lastWrongAt
  }
}

function mapStudyRecord(record: ApiStudyRecord): StudyRecord {
  return {
    date: record.date,
    questionsCompleted: record.questions_completed,
    totalScore: record.total_score
  }
}

export const questionService = {
  async getRandomQuestion(module?: string, difficulty?: number): Promise<Question> {
    const data = await request.get<ApiQuestion, ApiQuestion>('/questions/random', {
      params: { module, difficulty }
    })
    return mapQuestion(data)
  },

  async submitAnswer(questionId: number, answer: string, answerTime: number): Promise<AnswerResult> {
    return request.post<AnswerResult, AnswerResult>('/answers', {
      question_id: questionId,
      answer,
      answer_time: answerTime
    })
  },

  async getProgress(): Promise<ProgressData> {
    return request.get<ProgressData, ProgressData>('/progress')
  },

  async getAchievements(): Promise<any[]> {
    return request.get<any[], any[]>('/achievements')
  },

  async getWrongQuestions(page = 1, pageSize = 20): Promise<WrongQuestionsResponse> {
    const data = await request.get<WrongQuestionsResponse, WrongQuestionsResponse>(
      '/wrong-questions',
      { params: { page, pageSize } }
    )
    return {
      ...data,
      items: (data.items ?? []).map(mapWrongQuestion)
    }
  },

  async removeWrongQuestion(id: number): Promise<void> {
    await request.delete(`/wrong-questions/${id}`)
  },

  async getStudyRecords(year?: number, month?: number): Promise<StudyRecordsResponse> {
    const data = await request.get<ApiStudyRecordsResponse, ApiStudyRecordsResponse>(
      '/study-records',
      {
        params: {
          year,
          month
        }
      }
    )

    return {
      records: (data.records ?? []).map(mapStudyRecord),
      totalDays: data.total_days,
      consecutiveDays: data.consecutive_days
    }
  }
}
