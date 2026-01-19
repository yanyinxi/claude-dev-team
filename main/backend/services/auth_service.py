"""
认证服务
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.db import User
from models.schema import StudentLoginRequest, AdminLoginRequest, LoginResponse, UserResponse
from core.security import verify_password, create_access_token
from core.config import settings
from core.exceptions import UnauthorizedException


class AuthService:
    """认证服务类"""

    @staticmethod
    async def student_login(request: StudentLoginRequest, db: AsyncSession) -> LoginResponse:
        """
        学生登录
        如果昵称不存在则自动创建账号
        """
        # 查询用户是否存在
        result = await db.execute(
            select(User).where(User.nickname == request.nickname, User.role == "student")
        )
        user = result.scalar_one_or_none()

        # 如果不存在则创建新用户
        if not user:
            user = User(
                nickname=request.nickname,
                role="student",
                total_score=0
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # 生成JWT Token
        token = create_access_token(data={"sub": user.id})

        return LoginResponse(
            user=UserResponse.model_validate(user),
            token=token
        )

    @staticmethod
    async def admin_login(request: AdminLoginRequest, db: AsyncSession) -> LoginResponse:
        """
        管理员登录
        验证用户名和密码
        """
        # 验证用户名
        if request.username != settings.ADMIN_USERNAME:
            raise UnauthorizedException("用户名或密码错误")

        # 查询管理员用户
        result = await db.execute(
            select(User).where(
                User.role == "admin",
                User.nickname == request.username
            )
        )
        admin = result.scalar_one_or_none()

        if not admin:
            raise UnauthorizedException("管理员账号不存在")

        # 验证密码
        if not verify_password(request.password, admin.password_hash):
            raise UnauthorizedException("用户名或密码错误")

        # 生成JWT Token
        token = create_access_token(data={"sub": admin.id})

        return LoginResponse(
            user=UserResponse.model_validate(admin),
            token=token
        )
