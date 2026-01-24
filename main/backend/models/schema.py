"""
Pydantic数据模型 - 请求和响应模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ============ 用户相关模型 ============


class UserBase(BaseModel):
    """用户基础模型"""

    nickname: str = Field(..., min_length=2, max_length=20, description="用户昵称")


class StudentLoginRequest(UserBase):
    """学生登录请求"""

    pass


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""

    username: str = Field(..., description="管理员用户名")
    password: str = Field(..., description="管理员密码")


class UserResponse(BaseModel):
    """用户响应模型"""

    id: int
    nickname: str
    role: str
    total_score: int
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """登录响应"""

    user: UserResponse
    token: str


# ============ 题目相关模型 ============


class QuestionBase(BaseModel):
    """题目基础模型"""

    module: str = Field(..., description="模块: vocabulary/grammar/reading")
    difficulty: int = Field(..., ge=1, le=5, description="难度等级 1-5")
    question_text: str = Field(..., description="题目文本")
    question_image: Optional[str] = Field(None, description="题目图片URL")
    option_a: str = Field(..., description="选项A")
    option_b: str = Field(..., description="选项B")
    option_c: Optional[str] = Field(None, description="选项C")
    option_d: Optional[str] = Field(None, description="选项D")
    explanation: Optional[str] = Field(None, description="答案解析")


class QuestionResponse(QuestionBase):
    """题目响应模型（不包含正确答案）"""

    id: int

    class Config:
        from_attributes = True


class QuestionWithAnswer(QuestionResponse):
    """题目响应模型（包含正确答案，仅管理员）"""

    correct_answer: str

    class Config:
        from_attributes = True


# ============ 答题相关模型 ============


class AnswerRequest(BaseModel):
    """答题请求"""

    question_id: int = Field(..., description="题目ID")
    answer: str = Field(..., pattern="^[A-D]$", description="用户答案 A/B/C/D")
    answer_time: int = Field(..., ge=0, description="答题时间(秒)")


class AchievementResponse(BaseModel):
    """成就响应"""

    id: int
    name: str
    description: Optional[str]
    badge_icon: Optional[str]

    class Config:
        from_attributes = True


class AnswerResponse(BaseModel):
    """答题响应"""

    is_correct: bool
    correct_answer: str
    explanation: Optional[str]
    score: int
    streak: int
    total_score: int
    new_achievements: List[AchievementResponse] = []
    encouragement: str


# ============ 进度相关模型 ============


class ProgressResponse(BaseModel):
    """学习进度响应"""

    total_questions: int
    correct_answers: int
    accuracy: float
    streak: int
    daily_goal: int = 20
    completed_today: int


class WrongQuestionResponse(BaseModel):
    """错题响应"""

    id: int
    question_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: Optional[str]
    option_d: Optional[str]
    correct_answer: str
    explanation: Optional[str]
    module: str
    difficulty: int
    wrong_count: int
    last_wrong_at: datetime

    class Config:
        from_attributes = True


class WrongQuestionsListResponse(BaseModel):
    """错题列表响应"""

    items: List[WrongQuestionResponse]
    total: int
    page: int
    page_size: int


class StudyRecordResponse(BaseModel):
    """学习记录响应（用于日历）"""

    date: str
    questions_completed: int
    total_score: int


class StudyRecordsResponse(BaseModel):
    """学习记录列表响应"""

    records: List[StudyRecordResponse]
    total_days: int
    consecutive_days: int


# ============ 抢答相关模型 ============


class SpeedQuizStartRequest(BaseModel):
    """开始抢答请求"""
    difficulty: int = Field(..., ge=1, le=5, description="难度等级 1-5")
    module: str = Field(..., description="模块: vocabulary/grammar/reading")
    rounds: int = Field(..., ge=5, le=20, description="题目数量")


class SpeedQuizSubmitRequest(BaseModel):
    """提交答案请求"""
    battle_id: int = Field(..., description="对战ID")
    question_id: int = Field(..., description="题目ID")
    answer: str = Field(..., pattern="^[A-D]$", description="用户答案")
    answer_time: int = Field(..., ge=0, description="答题时间(毫秒)")


class SpeedQuizStartResponse(BaseModel):
    """开始抢答响应"""
    battle_id: int
    question: QuestionResponse


class SpeedQuizSubmitResponse(BaseModel):
    """提交答案响应"""
    is_correct: bool
    ai_answer: str
    ai_time: int
    correct_answer: str
    winner: str
    next_question: Optional[QuestionResponse]


class SpeedQuizStatsResponse(BaseModel):
    """抢答战绩响应"""
    total_battles: int
    wins: int
    losses: int
    win_rate: float
    fastest_time: int
    max_streak: int


class SpeedQuizBattleResponse(BaseModel):
    """抢答对战记录响应"""
    id: int
    difficulty: int
    module: str
    user_wins: int
    ai_wins: int
    created_at: datetime

    class Config:
        from_attributes = True


class SpeedQuizHistoryResponse(BaseModel):
    """抢答历史响应"""
    battles: List[SpeedQuizBattleResponse]
    total: int
    page: int
    page_size: int


# ============ 通用响应模型 ============


class ApiResponse(BaseModel):
    """统一API响应格式"""

    code: int = 200
    message: str = "success"
    data: Optional[dict] = None


# ============ 闹钟相关模型 ============


class AlarmRuleCreate(BaseModel):
    """创建闹钟规则请求"""
    rule_type: str = Field(..., pattern="^(global|personal)$", description="规则类型: global/personal")
    student_nickname: Optional[str] = Field(None, description="学生昵称（个性化规则必填）")
    study_duration: int = Field(..., ge=1, le=120, description="学习时长（分钟）")
    rest_duration: int = Field(..., ge=1, le=60, description="休息时长（分钟）")


class AlarmRuleUpdate(BaseModel):
    """更新闹钟规则请求"""
    study_duration: Optional[int] = Field(None, ge=1, le=120, description="学习时长（分钟）")
    rest_duration: Optional[int] = Field(None, ge=1, le=60, description="休息时长（分钟）")
    is_active: Optional[bool] = Field(None, description="是否启用")


class AlarmRuleResponse(BaseModel):
    """闹钟规则响应"""
    id: int
    rule_type: str
    student_nickname: Optional[str]
    study_duration: int
    rest_duration: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlarmStatusResponse(BaseModel):
    """学习状态响应"""
    session_type: str = Field(..., description="会话类型: studying/resting/idle")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    remaining_seconds: int = Field(..., description="剩余秒数")
    is_blocked: bool = Field(..., description="是否被阻止操作")
    rule: Optional[AlarmRuleResponse] = Field(None, description="生效的规则")


class AlarmValidateResponse(BaseModel):
    """验证响应"""
    can_operate: bool = Field(..., description="是否可以操作")
    reason: Optional[str] = Field(None, description="不能操作的原因")
    remaining_seconds: int = Field(0, description="剩余休息秒数")
