"""
简化版系统进化测试

用于快速验证进化机制的基本功能
"""

import pytest
from pathlib import Path
import sys

# 添加项目路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / ".claude" / "hooks" / "scripts"))
sys.path.insert(0, str(project_root / "main" / "backend"))


class TestSimpleEvolution:
    """简化版进化测试"""

    def test_auto_evolver_import(self):
        """测试 AutoEvolver 能否正常导入"""
        try:
            from auto_evolver import AutoEvolver
            assert AutoEvolver is not None
            print("✅ AutoEvolver 导入成功")
        except ImportError as e:
            pytest.fail(f"❌ AutoEvolver 导入失败: {e}")

    def test_intelligence_calculator_import(self):
        """测试 IntelligenceCalculator 能否正常导入"""
        try:
            from services.monitor_intelligence import IntelligenceCalculator
            assert IntelligenceCalculator is not None
            print("✅ IntelligenceCalculator 导入成功")
        except ImportError as e:
            pytest.fail(f"❌ IntelligenceCalculator 导入失败: {e}")

    def test_quality_evaluation(self):
        """测试质量评估功能"""
        from auto_evolver import AutoEvolver
        
        evolver = AutoEvolver(project_root)
        
        # 测试成功任务
        result_success = {
            'duration': 45,
            'files_modified': ['test1.py', 'test2.py', 'test3.py'],
            'success': True,
            'parallel_execution': False
        }
        score_success = evolver.evaluate_quality(result_success)
        assert 7.0 <= score_success <= 10.0, f"成功任务分数异常: {score_success}"
        print(f"✅ 成功任务评分: {score_success:.1f}/10")
        
        # 测试失败任务
        result_failure = {
            'duration': 300,
            'files_modified': [],
            'success': False,
            'parallel_execution': False
        }
        score_failure = evolver.evaluate_quality(result_failure)
        assert 0.0 <= score_failure < 7.0, f"失败任务分数异常: {score_failure}"
        print(f"✅ 失败任务评分: {score_failure:.1f}/10")

    def test_insight_extraction(self):
        """测试洞察提取功能"""
        from auto_evolver import AutoEvolver
        
        evolver = AutoEvolver(project_root)
        
        result = {
            'duration': 45,
            'files_modified': [
                'main/frontend/components/UserCard.vue',
                'main/backend/api/routes/user_router.py'
            ],
            'success': True,
            'parallel_execution': True
        }
        
        # 前端开发者
        insights_frontend = evolver.extract_insights(result, 'frontend-developer')
        assert len(insights_frontend) > 0, "前端洞察为空"
        assert any('组件' in i for i in insights_frontend), "缺少组件相关洞察"
        print(f"✅ 前端洞察: {insights_frontend}")
        
        # 后端开发者
        insights_backend = evolver.extract_insights(result, 'backend-developer')
        assert len(insights_backend) > 0, "后端洞察为空"
        assert any('API' in i for i in insights_backend), "缺少 API 相关洞察"
        print(f"✅ 后端洞察: {insights_backend}")

    def test_agent_strategy_mapping(self):
        """测试 Agent 到策略的映射"""
        from auto_evolver import AutoEvolver
        
        evolver = AutoEvolver(project_root)
        
        mappings = {
            'frontend-developer': 'frontend',
            'backend-developer': 'backend',
            'orchestrator': 'collaboration',
            'test': 'testing',
            'unknown-agent': 'unknown'
        }
        
        for agent, expected_strategy in mappings.items():
            strategy = evolver.map_agent_to_strategy(agent)
            assert strategy == expected_strategy, \
                f"映射错误: {agent} -> {strategy} (期望: {expected_strategy})"
        
        print("✅ Agent 策略映射正确")

    def test_intelligence_score_range(self):
        """测试智能水平分数范围"""
        from services.monitor_intelligence import IntelligenceCalculator
        
        calculator = IntelligenceCalculator()
        score = calculator.calculate_intelligence_score()
        
        # 验证总分范围
        assert 0 <= score.intelligence_score <= 10, \
            f"智能水平超出范围: {score.intelligence_score}"
        
        # 验证各项指标范围
        assert 0 <= score.strategy_weight <= 1, \
            f"策略权重超出范围: {score.strategy_weight}"
        assert 0 <= score.knowledge_richness <= 1, \
            f"知识丰富度超出范围: {score.knowledge_richness}"
        assert 0 <= score.quality_trend <= 1, \
            f"质量趋势超出范围: {score.quality_trend}"
        assert 0 <= score.evolution_frequency <= 1, \
            f"进化频率超出范围: {score.evolution_frequency}"
        
        print(f"✅ 智能水平: {score.intelligence_score:.2f}/10")
        print(f"   - 策略权重: {score.strategy_weight:.2f}")
        print(f"   - 知识丰富度: {score.knowledge_richness:.2f}")
        print(f"   - 质量趋势: {score.quality_trend:.2f}")
        print(f"   - 进化频率: {score.evolution_frequency:.2f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
