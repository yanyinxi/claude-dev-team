# 数据库路径配置修复说明

## 问题描述

原始配置使用相对路径 `sqlite+aiosqlite:///main/backend/db/ket_exam.db`，这导致：
- 从项目根目录运行时正常工作
- 从 `main/backend` 目录运行时失败（找不到数据库文件）
- 从其他子目录运行时也会失败

## 解决方案

修改 `main/backend/core/config.py`，实现智能路径解析：

### 核心改进

1. **添加 `get_project_root()` 静态方法**
   - 从当前文件向上查找，直到找到 `.git` 或 `CLAUDE.md`
   - 如果找不到，使用当前文件向上 3 级作为后备方案
   - 返回项目根目录的绝对路径

2. **将 `DATABASE_URL` 改为 `@property`**
   - 动态计算数据库文件的绝对路径
   - 使用 `get_project_root()` 确保路径始终正确
   - 格式：`sqlite+aiosqlite:///{绝对路径}`

### 代码示例

```python
from pathlib import Path

class Settings(BaseSettings):
    @staticmethod
    def get_project_root() -> Path:
        """智能查找项目根目录"""
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists() or (parent / 'CLAUDE.md').exists():
                return parent
        return Path(__file__).resolve().parent.parent.parent

    @property
    def DATABASE_URL(self) -> str:
        """数据库连接 URL（使用绝对路径）"""
        db_path = self.get_project_root() / "main" / "backend" / "db" / "ket_exam.db"
        return f"sqlite+aiosqlite:///{db_path}"
```

## 测试结果

运行 `tests/test_config_path.py` 验证：

### 测试场景

1. 从项目根目录运行 ✅
2. 从 `main/backend` 目录运行 ✅
3. 从 `tests` 目录运行 ✅

### 测试输出

```
数据库 URL: sqlite+aiosqlite:////Users/.../claude-dev-team/main/backend/db/ket_exam.db
路径是否为绝对路径: True
数据库文件是否存在: True
项目根目录: /Users/.../claude-dev-team
```

## 优势

1. **跨目录兼容**：从任何目录运行都能正确找到数据库
2. **智能查找**：自动识别项目根目录（通过 `.git` 或 `CLAUDE.md`）
3. **后备方案**：即使找不到标记文件，也能通过相对层级定位
4. **绝对路径**：避免相对路径的歧义性
5. **易于维护**：路径逻辑集中在一个方法中

## 使用方法

配置修改后，无需任何额外操作，直接使用：

```python
from core.config import settings

# 自动获取正确的数据库路径
db_url = settings.DATABASE_URL
```

## 注意事项

- 确保项目根目录存在 `.git` 或 `CLAUDE.md` 文件
- 如果移动项目结构，路径会自动适配
- 数据库文件必须位于 `main/backend/db/` 目录下
