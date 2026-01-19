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


# ============ 通用响应模型 ============


class ApiResponse(BaseModel):
    """统一API响应格式"""

    code: int = 200
    message: str = "success"
    data: Optional[dict] = None
