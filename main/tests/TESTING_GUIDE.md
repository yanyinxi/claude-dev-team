# 系统进化能力测试指南

本指南介绍如何测试 Claude Dev Team 的自进化能力。

---

## 快速开始

### 1. 运行简化版测试（推荐）

简化版测试验证核心功能，无需额外依赖：

```bash
cd /Users/yanyinxi/工作/code/Java/claudecode/claude-dev-team
python3 -m pytest main/tests/integration/test_simple_evolution.py -v -s
```

**预期结果**: 6 个测试全部通过

### 2. 运行完整进化循环测试

完整测试模拟真实的进化场景，需要安装额外依赖：

```bash
# 安装依赖
pip3 install -r main/tests/requirements.txt

# 运行测试
python3 -m pytest main/tests/integration/test_system_evolution.py -v -s
```

**预期结果**: 智能水平提升至少 0.5 分

---

## 测试文件说明

### test_simple_evolution.py - 简化版测试

**目标**: 快速验证核心功能

**测试用例**:
1. `test_auto_evolver_import` - 验证进化引擎导入
2. `test_intelligence_calculator_import` - 验证智能计算器导入
3. `test_quality_evaluation` - 验证质量评估算法
4. `test_insight_extraction` - 验证洞察提取功能
5. `test_agent_strategy_mapping` - 验证 Agent 策略映射
6. `test_intelligence_score_range` - 验证智能水平计算

**优点**:
- ✅ 无需额外依赖
- ✅ 执行速度快（0.15秒）
- ✅ 验证核心功能

**缺点**:
- ❌ 不测试完整进化循环
- ❌ 不验证智能水平提升

### test_system_evolution.py - 完整进化测试

**目标**: 验证完整的进化循环

**测试用例**:
1. `test_evolution_cycle` - 完整进化循环测试
2. `test_strategy_rules_format` - 策略规则文件格式测试
3. `test_intelligence_calculation` - 智能水平计算测试

**优点**:
- ✅ 测试完整进化流程
- ✅ 验证智能水平提升
- ✅ 验证策略规则更新

**缺点**:
- ❌ 需要安装 pytest-asyncio
- ❌ 执行时间较长

---

## 测试结果解读

### 智能水平分数

| 分数范围 | 等级 | 说明 |
|---------|------|------|
| 8.0-10.0 | 优秀 | 系统高度智能化，策略丰富 |
| 6.0-7.9 | 良好 | 系统智能化程度较高 |
| 4.0-5.9 | 中等 | 系统有一定智能化能力 |
| 2.0-3.9 | 较低 | 系统智能化程度较低 |
| 0.0-1.9 | 初始 | 系统刚初始化，缺乏经验 |

### 各项指标说明

| 指标 | 说明 | 数据来源 |
|------|------|---------|
| **策略权重** | 策略规则的数量和质量 | `.claude/rules/*.md` |
| **知识丰富度** | Agent、Skill、最佳实践的数量 | `.claude/agents/`, `.claude/skills/`, `project_standards.md` |
| **质量趋势** | 代码审查通过率和测试覆盖率 | `main/docs/reviews/*.md` |
| **进化频率** | 最近 7 天的进化记录数量 | `.claude/rules/*.md` 更新时间 |

---

## 常见问题

### 1. 导入错误

**问题**: `ModuleNotFoundError: No module named 'hooks'`

**解决**: 
```python
# 在测试文件开头添加
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / ".claude" / "hooks" / "scripts"))
```

### 2. pytest-asyncio 未安装

**问题**: `ImportError: Error importing plugin "pytest_asyncio"`

**解决**:
```bash
pip3 install pytest-asyncio
```

或者运行简化版测试（不需要 pytest-asyncio）。

### 3. 智能水平分数为 0

**问题**: 智能水平计算结果为 0

**原因**: 
- 项目刚初始化，缺少策略规则
- 缺少 Agent 和 Skill 配置
- 缺少代码审查记录

**解决**: 
1. 执行一些任务，触发进化机制
2. 添加 Agent 和 Skill 配置
3. 添加代码审查记录

---

## 测试最佳实践

### 1. 测试前准备

```bash
# 确保项目结构完整
ls -la .claude/rules/
ls -la .claude/agents/
ls -la .claude/skills/

# 确保有一些历史数据
ls -la main/docs/reviews/
```

### 2. 测试后验证

```bash
# 查看新生成的策略规则
cat .claude/rules/frontend.md
cat .claude/rules/backend.md

# 查看智能水平变化
python3 -c "
from services.monitor_intelligence import IntelligenceCalculator
calculator = IntelligenceCalculator()
score = calculator.calculate_intelligence_score()
print(f'智能水平: {score.intelligence_score:.2f}/10')
"
```

### 3. 持续测试

建议定期运行测试，监控系统进化效果：

```bash
# 每周运行一次
./main/tests/run_tests.sh

# 或者添加到 CI/CD 流程
pytest main/tests/integration/ --tb=short
```

---

## 测试报告

测试报告保存在 `main/docs/test_reports/` 目录：

- `simple_evolution_test_summary.md` - 简化版测试总结
- `system_evolution_test_report.md` - 完整测试报告模板

---

## 相关文档

- [测试文档](./README.md)
- [项目标准](.claude/project_standards.md)
- [进化机制](.claude/hooks/scripts/auto_evolver.py)
- [智能计算](main/backend/services/monitor_intelligence.py)

---

## 联系方式

如有问题，请参考：
- [项目文档](../docs/)
- [GitHub Issues](https://github.com/your-repo/issues)
