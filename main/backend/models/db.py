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
