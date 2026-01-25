"""
SQLAlchemy数据库模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False, index=True)
    role = Column(String(20), default="student")  # student/admin
    password_hash = Column(String(255), nullable=True)  # 管理员密码
    total_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    progress = relationship("UserProgress", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    wrong_questions = relationship("WrongQuestion", back_populates="user")


class Question(Base):
    """题目表"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(20), nullable=False, index=True)  # vocabulary/grammar/reading
    difficulty = Column(Integer, default=1)  # 1-5难度等级
    question_text = Column(Text, nullable=False)
    question_image = Column(String(255), nullable=True)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=True)
    option_d = Column(Text, nullable=True)
    correct_answer = Column(String(1), nullable=False)  # A/B/C/D
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    progress = relationship("UserProgress", back_populates="question")
    wrong_questions = relationship("WrongQuestion", back_populates="question")


class UserProgress(Base):
    """学习进度表"""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answer_time = Column(Integer, nullable=True)  # 答题时间(秒)
    answered_at = Column(DateTime, default=datetime.utcnow, index=True)

    # 关系
    user = relationship("User", back_populates="progress")
    question = relationship("Question", back_populates="progress")


class Achievement(Base):
    """成就表"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    badge_icon = Column(String(255), nullable=True)
    requirement_type = Column(String(50), nullable=False)  # total_questions/streak/daily_login
    requirement_value = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """用户成就关联表"""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    # 唯一约束
    __table_args__ = (UniqueConstraint('user_id', 'achievement_id', name='uq_user_achievement'),)

    # 关系
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class WrongQuestion(Base):
    """错题本表"""
    __tablename__ = "wrong_questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    wrong_count = Column(Integer, default=1)
    last_wrong_at = Column(DateTime, default=datetime.utcnow)

    # 唯一约束
    __table_args__ = (UniqueConstraint('user_id', 'question_id', name='uq_user_wrong_question'),)

    # 关系
    user = relationship("User", back_populates="wrong_questions")
    question = relationship("Question", back_populates="wrong_questions")


class SpeedQuizBattle(Base):
    """抢答对战记录表"""
    __tablename__ = "speed_quiz_battles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    difficulty = Column(Integer, nullable=False)
    module = Column(String(20), nullable=False)
    total_questions = Column(Integer, nullable=False)
    user_correct = Column(Integer, default=0)
    ai_correct = Column(Integer, default=0)
    user_wins = Column(Integer, default=0)
    ai_wins = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # 关系
    details = relationship("SpeedQuizDetail", back_populates="battle")


class SpeedQuizDetail(Base):
    """抢答详细记录表"""
    __tablename__ = "speed_quiz_details"

    id = Column(Integer, primary_key=True, index=True)
    battle_id = Column(Integer, ForeignKey("speed_quiz_battles.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String(1), nullable=True)
    user_time = Column(Integer, nullable=True)  # 毫秒
    ai_answer = Column(String(1), nullable=False)
    ai_time = Column(Integer, nullable=False)  # 毫秒
    correct_answer = Column(String(1), nullable=False)
    winner = Column(String(10), nullable=False)  # user/ai/tie
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    battle = relationship("SpeedQuizBattle", back_populates="details")


class AlarmRule(Base):
    """闹钟规则表"""
    __tablename__ = "alarm_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_type = Column(String(20), nullable=False, index=True)  # global/personal
    student_nickname = Column(String(50), nullable=True, index=True)  # 个性化规则的学生昵称
    study_duration = Column(Integer, nullable=False)  # 学习时长（分钟）
    rest_duration = Column(Integer, nullable=False)  # 休息时长（分钟）
    is_active = Column(Boolean, default=True)  # 是否启用
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    sessions = relationship("AlarmSession", back_populates="rule")


class AlarmSession(Base):
    """学习会话表"""
    __tablename__ = "alarm_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_type = Column(String(20), nullable=False)  # studying/resting
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    rule_id = Column(Integer, ForeignKey("alarm_rules.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    user = relationship("User")
    rule = relationship("AlarmRule", back_populates="sessions")


class MonitorIntelligence(Base):
    """智能水平历史记录表

    记录系统智能水平的演化历史，用于监控系统的学习和进化能力。
    智能水平由多个维度组成：策略权重、知识丰富度、质量趋势、进化频率。
    """
    __tablename__ = "monitor_intelligence"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)  # 记录时间（带索引）
    intelligence_score = Column(Integer, nullable=False)  # 智能水平总分 (0-10)
    strategy_weight = Column(Integer, nullable=False)  # 策略权重 (0-1)
    knowledge_richness = Column(Integer, nullable=False)  # 知识丰富度 (0-1)
    quality_trend = Column(Integer, nullable=False)  # 质量趋势 (0-1)
    evolution_frequency = Column(Integer, nullable=False)  # 进化频率 (0-1)
    milestone_event = Column(Text, nullable=True)  # 里程碑事件（可选）
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class MonitorDiagnosis(Base):
    """诊断记录表

    记录系统自动诊断发现的问题，包括性能、安全、质量、架构等方面。
    支持自动修复和手动修复，跟踪问题状态。
    """
    __tablename__ = "monitor_diagnosis"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)  # 诊断时间（带索引）
    issue_id = Column(String(50), nullable=False, unique=True)  # 问题唯一标识
    severity = Column(String(20), nullable=False, index=True)  # 严重程度: Critical/Important/Suggestion（带索引）
    category = Column(String(50), nullable=False, index=True)  # 问题分类: performance/security/quality/architecture（带索引）
    title = Column(String(200), nullable=False)  # 问题标题
    description = Column(Text, nullable=False)  # 问题描述
    location = Column(String(500), nullable=True)  # 文件位置
    suggestion = Column(Text, nullable=True)  # 修复建议
    auto_fixable = Column(Boolean, default=False)  # 是否可自动修复
    fix_code = Column(Text, nullable=True)  # 修复代码
    status = Column(String(20), default="open")  # 状态: open/fixed/ignored
    fixed_at = Column(DateTime, nullable=True)  # 修复时间
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class MonitorAgentPerformance(Base):
    """Agent 性能记录表

    记录各个 Agent 的任务执行情况，包括任务状态、进度、耗时、成功率等。
    用于监控 Agent 的工作效率和健康状态。
    """
    __tablename__ = "monitor_agent_performance"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False, index=True)  # Agent 名称（带索引）
    agent_type = Column(String(50), nullable=False)  # Agent 类型: developer/reviewer/tester/orchestrator
    task_id = Column(String(100), nullable=True)  # 任务 ID
    status = Column(String(20), nullable=False)  # 状态: working/completed/failed
    progress = Column(Integer, default=0)  # 进度 (0-100)
    duration_seconds = Column(Integer, nullable=True)  # 任务耗时（秒）
    success = Column(Boolean, nullable=True)  # 是否成功
    error_message = Column(Text, nullable=True)  # 错误信息
    started_at = Column(DateTime, nullable=False, index=True)  # 开始时间（带索引）
    completed_at = Column(DateTime, nullable=True)  # 完成时间
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
