"""
系统进化能力集成测试

测试目标：
1. 验证系统能够从任务执行中学习
2. 验证智能水平能够提升
3. 验证策略规则能够自动更新
4. 验证知识库能够自动扩充

测试场景：
- 模拟 3 轮任务执行（前端、后端、测试）
- 触发进化机制
- 验证智能水平提升
- 验证策略和知识增加
"""

import pytest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class TestSystemEvolution:
    """测试系统自进化能力"""

    @pytest.fixture
    def project_root(self):
        """创建临时项目目录"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # 创建必要的目录结构
        (project_path / ".claude" / "rules").mkdir(parents=True, exist_ok=True)
        (project_path / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
        (project_path / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        (project_path / "main" / "docs" / "reviews").mkdir(parents=True, exist_ok=True)
        
        # 创建初始配置文件
        self._create_initial_files(project_path)
        
        yield project_path
        
        # 清理临时目录
        shutil.rmtree(temp_dir)

    def _create_initial_files(self, project_root: Path):
        """创建初始配置文件"""
        # 创建 project_standards.md
        standards_file = project_root / ".claude" / "project_standards.md"
        standards_file.write_text("""
# 项目技术标准

## 最佳实践

### 测试驱动开发
- 先写测试，再写实现

### 代码审查
- 所有代码必须经过审查

## 进化记录

### 2026-01-20 v1.0.0
- **变更类型**: 初始化
- **变更内容**: 项目初始化
""", encoding="utf-8")

        # 创建初始 Agent 配置
        agent_file = project_root / ".claude" / "agents" / "frontend-developer.md"
        agent_file.write_text("""
# Frontend Developer Agent

## 职责
- 前端开发
- UI 组件实现
""", encoding="utf-8")

        # 创建初始 Skill
        skill_dir = project_path / ".claude" / "skills" / "testing"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("""
# Testing Skill

## 功能
- 单元测试
- 集成测试
""", encoding="utf-8")

    @pytest.fixture
    async def initial_state(self, project_root):
        """记录初始状态"""
        from services.monitor_intelligence import IntelligenceCalculator
        
        # 临时修改项目根目录
        original_root = IntelligenceCalculator.__init__
        IntelligenceCalculator.__init__ = lambda self: setattr(self, 'project_root', project_root)
        
        calculator = IntelligenceCalculator()
        initial_score = calculator.calculate_intelligence_score()
        
        # 恢复原始方法
        IntelligenceCalculator.__init__ = original_root
        
        # 统计初始数据
        rules_dir = project_root / ".claude" / "rules"
        initial_strategies = len(list(rules_dir.glob("*.md"))) if rules_dir.exists() else 0
        
        agents_dir = project_root / ".claude" / "agents"
        initial_agents = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0
        
        return {
            'intelligence': initial_score.intelligence_score,
            'strategies': initial_strategies,
            'agents': initial_agents,
            'strategy_weight': initial_score.strategy_weight,
            'knowledge_richness': initial_score.knowledge_richness
        }

    async def test_evolution_cycle(self, project_root, initial_state):
        """测试完整的进化循环"""
        
        # 1. 模拟任务执行
        tasks = [
            self._simulate_frontend_task(),
            self._simulate_backend_task(),
            self._simulate_test_task()
        ]
        
        execution_results = []
        for task in tasks:
            result = await task
            execution_results.append(result)
            # 记录执行结果
            await self._record_execution_result(project_root, result)
        
        # 2. 触发进化
        await self._trigger_evolution(project_root, execution_results)
        
        # 3. 验证进化效果
        from services.monitor_intelligence import IntelligenceCalculator
        
        # 临时修改项目根目录
        original_root = IntelligenceCalculator.__init__
        IntelligenceCalculator.__init__ = lambda self: setattr(self, 'project_root', project_root)
        
        calculator = IntelligenceCalculator()
        final_score = calculator.calculate_intelligence_score()
        
        # 恢复原始方法
        IntelligenceCalculator.__init__ = original_root
        
        # 验证智能水平提升
        assert final_score.intelligence_score > initial_state['intelligence'] + 0.5, \
            f"智能水平未提升：初始 {initial_state['intelligence']}, 最终 {final_score.intelligence_score}"
        
        # 验证策略数量增加
        rules_dir = project_root / ".claude" / "rules"
        final_strategies = len(list(rules_dir.glob("*.md"))) if rules_dir.exists() else 0
        assert final_strategies > initial_state['strategies'], \
            f"策略数量未增加：初始 {initial_state['strategies']}, 最终 {final_strategies}"
        
        # 验证知识丰富度提升
        assert final_score.knowledge_richness > initial_state['knowledge_richness'], \
            f"知识丰富度未提升：初始 {initial_state['knowledge_richness']}, 最终 {final_score.knowledge_richness}"
        
        # 验证进化频率 > 0
        assert final_score.evolution_frequency > 0, \
            f"进化频率为 0：{final_score.evolution_frequency}"
        
        print(f"\n✅ 进化测试通过:")
        print(f"  智能水平: {initial_state['intelligence']:.2f} → {final_score.intelligence_score:.2f} (+{final_score.intelligence_score - initial_state['intelligence']:.2f})")
        print(f"  策略数量: {initial_state['strategies']} → {final_strategies} (+{final_strategies - initial_state['strategies']})")
        print(f"  知识丰富度: {initial_state['knowledge_richness']:.2f} → {final_score.knowledge_richness:.2f} (+{final_score.knowledge_richness - initial_state['knowledge_richness']:.2f})")
        print(f"  进化频率: {final_score.evolution_frequency:.2f}")

    async def _simulate_frontend_task(self) -> Dict[str, Any]:
        """模拟前端任务执行"""
        return {
            'agent': 'frontend-developer',
            'task': '实现用户登录组件',
            'success': True,
            'duration': 45,
            'quality_score': 9.0,
            'files_modified': [
                'main/frontend/components/LoginForm.vue',
                'main/frontend/stores/userStore.ts',
                'main/frontend/services/authService.ts'
            ],
            'parallel_execution': False,
            'insights': [
                '组件拆分策略：按职责拆分，保持单一职责',
                'TypeScript 类型安全：为所有 props 添加类型定义',
                'Pinia 状态管理：使用 Composition API 风格'
            ]
        }

    async def _simulate_backend_task(self) -> Dict[str, Any]:
        """模拟后端任务执行"""
        return {
            'agent': 'backend-developer',
            'task': '实现用户认证 API',
            'success': True,
            'duration': 60,
            'quality_score': 8.5,
            'files_modified': [
                'main/backend/api/routes/auth_router.py',
                'main/backend/services/auth_service.py',
                'main/backend/models/schema.py',
                'main/backend/core/security.py'
            ],
            'parallel_execution': False,
            'insights': [
                '异步数据库操作：使用 async/await 避免阻塞',
                '统一错误处理：使用 AppException 及其子类',
                'JWT Token 生成：使用 HS256 算法加密'
            ]
        }

    async def _simulate_test_task(self) -> Dict[str, Any]:
        """模拟测试任务执行"""
        return {
            'agent': 'test',
            'task': '编写单元测试',
            'success': True,
            'duration': 30,
            'quality_score': 9.5,
            'files_modified': [
                'main/tests/backend/test_auth.py',
                'main/tests/frontend/LoginForm.test.ts'
            ],
            'parallel_execution': False,
            'insights': [
                '测试驱动开发：先写测试，再写实现',
                'Mock 策略：使用 pytest-mock 模拟外部依赖',
                '测试覆盖率：确保核心逻辑 100% 覆盖'
            ]
        }

    async def _record_execution_result(self, project_root: Path, result: Dict[str, Any]):
        """记录执行结果到文件"""
        results_dir = project_root / ".claude" / "execution_results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = results_dir / f"{result['agent']}_{timestamp}.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    async def _trigger_evolution(self, project_root: Path, execution_results: List[Dict[str, Any]]):
        """触发进化机制"""
        from hooks.scripts.auto_evolver import AutoEvolver
        
        evolver = AutoEvolver(project_root)
        
        for result in execution_results:
            # 评估质量
            quality_score = evolver.evaluate_quality(result)
            
            # 提取洞察
            insights = result.get('insights', [])
            if not insights:
                insights = evolver.extract_insights(result, result['agent'])
            
            # 更新 Rules 文件
            if insights:
                evolver.update_rules_file(result['agent'], quality_score, insights)
                print(f"✅ 进化完成: {result['agent']} 得分 {quality_score:.1f}/10")

    async def test_strategy_rules_format(self, project_root):
        """测试策略规则文件格式"""
        from hooks.scripts.auto_evolver import AutoEvolver
        
        evolver = AutoEvolver(project_root)
        
        # 模拟任务结果
        result = {
            'duration': 45,
            'files_modified': ['test1.py', 'test2.py'],
            'success': True,
            'parallel_execution': False
        }
        
        # 评估质量
        quality_score = evolver.evaluate_quality(result)
        assert 0 <= quality_score <= 10, f"质量分数超出范围: {quality_score}"
        
        # 提取洞察
        insights = ['测试洞察1', '测试洞察2']
        
        # 更新规则文件
        rules_file = evolver.update_rules_file('frontend-developer', quality_score, insights)
        
        # 验证文件存在
        assert rules_file.exists(), f"规则文件未创建: {rules_file}"
        
        # 验证文件格式
        content = rules_file.read_text(encoding='utf-8')
        assert '## 新学到的洞察' in content, "缺少洞察章节"
        assert '**更新时间**' in content, "缺少更新时间"
        assert '**策略关键词**' in content, "缺少策略关键词"
        
        print(f"✅ 策略规则文件格式正确: {rules_file}")

    async def test_intelligence_calculation(self, project_root):
        """测试智能水平计算"""
        from services.monitor_intelligence import IntelligenceCalculator
        
        # 临时修改项目根目录
        original_root = IntelligenceCalculator.__init__
        IntelligenceCalculator.__init__ = lambda self: setattr(self, 'project_root', project_root)
        
        calculator = IntelligenceCalculator()
        score = calculator.calculate_intelligence_score()
        
        # 恢复原始方法
        IntelligenceCalculator.__init__ = original_root
        
        # 验证分数范围
        assert 0 <= score.intelligence_score <= 10, f"智能水平超出范围: {score.intelligence_score}"
        assert 0 <= score.strategy_weight <= 1, f"策略权重超出范围: {score.strategy_weight}"
        assert 0 <= score.knowledge_richness <= 1, f"知识丰富度超出范围: {score.knowledge_richness}"
        assert 0 <= score.quality_trend <= 1, f"质量趋势超出范围: {score.quality_trend}"
        assert 0 <= score.evolution_frequency <= 1, f"进化频率超出范围: {score.evolution_frequency}"
        
        print(f"✅ 智能水平计算正确:")
        print(f"  总分: {score.intelligence_score:.2f}/10")
        print(f"  策略权重: {score.strategy_weight:.2f}")
        print(f"  知识丰富度: {score.knowledge_richness:.2f}")
        print(f"  质量趋势: {score.quality_trend:.2f}")
        print(f"  进化频率: {score.evolution_frequency:.2f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
