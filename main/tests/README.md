# 测试文档

## 目录结构

```
main/tests/
├── __init__.py                          # 测试包初始化
├── conftest.py                          # Pytest 配置
├── requirements.txt                     # 测试依赖
├── run_tests.sh                         # 测试运行脚本
├── README.md                            # 测试文档
├── backend/                             # 后端测试
│   └── test_auth.py                     # 认证测试
├── frontend/                            # 前端测试
│   └── LoginForm.test.ts                # 登录组件测试
└── integration/                         # 集成测试
    └── test_system_evolution.py         # 系统进化测试
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r main/tests/requirements.txt
```

### 2. 运行所有测试

```bash
./main/tests/run_tests.sh
```

### 3. 运行特定测试

```bash
# 运行集成测试
pytest main/tests/integration/ -v

# 运行单个测试文件
pytest main/tests/integration/test_system_evolution.py -v

# 运行特定测试方法
pytest main/tests/integration/test_system_evolution.py::TestSystemEvolution::test_evolution_cycle -v
```

## 测试说明

### 系统进化能力测试 (test_system_evolution.py)

**测试目标**：验证系统的自进化能力和智能水平提升。

**测试场景**：
1. 模拟 3 轮任务执行（前端、后端、测试）
2. 触发进化机制
3. 验证智能水平提升
4. 验证策略和知识增加

**测试用例**：

#### 1. test_evolution_cycle
完整的进化循环测试，验证：
- 智能水平从初始值提升至少 0.5 分
- 策略规则增加至少 3 条
- 知识条目增加
- 进化频率 > 0

#### 2. test_strategy_rules_format
验证策略规则文件格式正确：
- 包含"新学到的洞察"章节
- 包含更新时间
- 包含策略关键词

#### 3. test_intelligence_calculation
验证智能水平计算正确：
- 总分在 0-10 范围内
- 各项指标在 0-1 范围内
- 计算公式正确

**预期结果**：
- ✅ 智能水平提升至少 0.5 分
- ✅ 策略规则增加至少 3 条
- ✅ 知识条目增加
- ✅ 进化频率 > 0

## 测试覆盖率

运行测试并生成覆盖率报告：

```bash
pytest main/tests/ --cov=main/backend --cov-report=html
```

查看覆盖率报告：

```bash
open htmlcov/index.html
```

## 测试最佳实践

1. **测试独立性**：每个测试独立运行，不依赖其他测试
2. **使用 Fixture**：使用 pytest fixture 管理测试数据
3. **清理资源**：测试结束后清理临时文件和数据
4. **异步测试**：使用 pytest-asyncio 支持异步测试
5. **Mock 外部依赖**：使用 pytest-mock 模拟外部服务

## 常见问题

### 1. 导入错误

**问题**：`ModuleNotFoundError: No module named 'services'`

**解决**：确保 `conftest.py` 正确配置了 Python 路径。

### 2. 异步测试失败

**问题**：`RuntimeError: Event loop is closed`

**解决**：使用 `@pytest.mark.asyncio` 装饰器标记异步测试。

### 3. 临时文件未清理

**问题**：测试后留下临时文件

**解决**：使用 `yield` fixture 确保清理代码执行。

## 参考资料

- [Pytest 文档](https://docs.pytest.org/)
- [Pytest-asyncio 文档](https://pytest-asyncio.readthedocs.io/)
- [项目测试规范](.claude/project_standards.md)
