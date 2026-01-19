"""
创建管理员账号
"""
import asyncio
from sqlalchemy import select
from core.database import get_db
from core.security import get_password_hash
from models.db import User


async def create_admin():
    """创建管理员账号"""
    async for db in get_db():
        try:
            # 检查是否已存在admin账号
            result = await db.execute(select(User).where(User.nickname == "admin"))
            existing_admin = result.scalar_one_or_none()

            if existing_admin:
                print("❌ 管理员账号已存在")
                print(f"   昵称: {existing_admin.nickname}")
                print(f"   角色: {existing_admin.role}")
                return

            # 创建管理员账号
            admin = User(
                nickname="admin",
                role="admin",
                password_hash=get_password_hash("admin123")  # 默认密码
            )
            db.add(admin)
            await db.commit()

            print("✅ 管理员账号创建成功！")
            print("   昵称: admin")
            print("   密码: admin123")
            print("   角色: admin")

        except Exception as e:
            print(f"❌ 创建失败: {e}")
            await db.rollback()
        finally:
            break


if __name__ == "__main__":
    asyncio.run(create_admin())
