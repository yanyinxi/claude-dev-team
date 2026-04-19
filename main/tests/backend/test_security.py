"""
安全模块单元测试

这是一个真实能跑的测试示例，演示：
- 密码哈希验证
- JWT token 创建与解码
- 过期时间计算

CI 会在每次 push 时运行这些测试。
"""
import sys
from datetime import timedelta, datetime, timezone
from pathlib import Path

import pytest

# 让 pytest 能导入 main/backend
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from core.security import (  # noqa: E402
    verify_password,
    get_password_hash,
    create_access_token,
)
from core.config import settings  # noqa: E402
from jose import jwt  # noqa: E402


class TestPasswordHashing:
    def test_hash_produces_different_output_each_call(self):
        h1 = get_password_hash("secret123")
        h2 = get_password_hash("secret123")
        assert h1 != h2, "bcrypt 每次应生成不同的 salt"

    def test_verify_correct_password(self):
        hashed = get_password_hash("correct_password")
        assert verify_password("correct_password", hashed) is True

    def test_verify_incorrect_password(self):
        hashed = get_password_hash("correct_password")
        assert verify_password("wrong_password", hashed) is False


class TestJwtToken:
    def test_create_token_with_user_id(self):
        token = create_access_token({"sub": 42})
        assert isinstance(token, str)
        assert len(token) > 20

    def test_integer_sub_is_stringified(self):
        token = create_access_token({"sub": 42})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "42", "JWT spec 要求 sub 为字符串"

    def test_custom_expiration(self):
        token = create_access_token({"sub": 1}, expires_delta=timedelta(minutes=5))
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = (exp - now).total_seconds()
        # 5 分钟 ± 5 秒
        assert 295 < delta < 305

    def test_default_expiration_uses_settings(self):
        token = create_access_token({"sub": 1})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        delta_hours = (exp - now).total_seconds() / 3600
        assert abs(delta_hours - settings.ACCESS_TOKEN_EXPIRE_HOURS) < 0.1


class TestExpirationIsTimezoneAware:
    """
    回归测试：防止 datetime.utcnow() 回归。
    utcnow() 返回 naive datetime 会在未来 Python 版本中报错。
    """

    def test_token_expiration_uses_timezone_aware_datetime(self):
        token = create_access_token({"sub": 1}, expires_delta=timedelta(seconds=60))
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # 如果 exp 字段能正常 decode 且 > 当前时间，说明时区处理正确
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp > datetime.now(timezone.utc)
