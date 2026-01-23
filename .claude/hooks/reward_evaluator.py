#!/usr/bin/env python3
"""
奖励评估器 (Reward Evaluator)

职责：
1. 监听 PostToolUse 事件（Task 工具调用）
2. 计算任务完成奖励分数 (0-10分)
3. 存储经验到 experience_pool.json

使用 Claude Code 原生 Hook 机制实现，0% 重复造轮子。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def calculate_reward(agent_type: str, prompt: str, result: str) -> float:
    """
    计算任务完成奖励分数 (0-10分)。
    
    评分维度：
    - 任务完成度 (0-3分)
    - 协作效果 (0-2分)
    - 效率 (0-2分)
    - 代码质量 (0-3分)
    
    Args:
        agent_type: Agent 类型
        prompt: 任务描述
        result: 执行结果
    
    Returns:
        奖励分数 (0-10)
    """
    score = 0.0
    
    # 1. 任务完成度 (0-3 分)
    if "完成" in result or "success" in result.lower():
        score += 2.0
    if "高质量" in result or "high quality" in result.lower():
        score += 1.0
    if "完美" in result or "perfect" in result.lower():
        score += 0.5
    
    # 2. 协作效果 (0-2 分)
    if "团队协作" in prompt or "collaboration" in prompt.lower():
        if "配合" in result or "coordinated" in result.lower():
            score += 1.0
        if "沟通顺畅" in result or "smooth" in result.lower():
            score += 0.5
    if "并行" in result or "parallel" in result.lower():
        score += 0.5
    
    # 3. 效率 (0-2 分)
    if "快速" in result or "fast" in result.lower():
        score += 1.0
    if "按时完成" in result or "on time" in result.lower():
        score += 0.5
    if "提前" in result or "ahead" in result.lower():
        score += 0.5
    
    # 4. 代码质量 (0-3 分)
    if "测试通过" in result or "tests passed" in result.lower():
        score += 1.5
    if "代码审查通过" in result or "reviewed" in result.lower():
        score += 0.5
    if "无 bug" in result or "no bug" in result.lower():
        score += 0.5
    if "重构" in result or "refactor" in result.lower():
        score += 0.5
    
    return min(score, 10.0)


def save_experience(agent_type: str, prompt: str, reward: float, result: str) -> None:
    """
    保存经验到经验池。
    
    Args:
        agent_type: Agent 类型
        prompt: 任务描述
        reward: 奖励分数
        result: 执行结果
    """
    experience = {
        "agent": agent_type,
        "reward": reward,
        "timestamp": datetime.now().isoformat(),
        "prompt_hash": hash(prompt) % 1000000,
        "result_preview": result[:200] if result else "",
    }
    
    # 确定策略关键词（简化版）
    strategy_keyword = infer_strategy_keyword(prompt)
    if strategy_keyword:
        experience["strategy_keyword"] = strategy_keyword
    
    experience_file = Path(".claude/experience_pool.json")
    
    # 读取现有经验
    experiences = []
    if experience_file.exists():
        try:
            with open(experience_file, 'r', encoding='utf-8') as f:
                experiences = json.load(f)
        except (json.JSONDecodeError, IOError):
            experiences = []
    
    # 添加新经验
    experiences.append(experience)
    
    # 只保留最近的 1000 条
    experiences = experiences[-1000:]
    
    # 保存
    with open(experience_file, 'w', encoding='utf-8') as f:
        json.dump(experiences, f, indent=2, ensure_ascii=False)


def infer_strategy_keyword(prompt: str) -> Optional[str]:
    """
    从任务描述推断策略关键词。
    
    Args:
        prompt: 任务描述
    
    Returns:
        策略关键词或 None
    """
    prompt_lower = prompt.lower()
    
    if any(kw in prompt_lower for kw in ["前端", "ui", "组件", "页面", "frontend", "react"]):
        return "frontend"
    elif any(kw in prompt_lower for kw in ["后端", "api", "数据库", "backend", "server"]):
        return "backend"
    elif any(kw in prompt_lower for kw in ["测试", "test", "验证"]):
        return "testing"
    elif any(kw in prompt_lower for kw in ["登录", "认证", "auth", "login"]):
        return "authentication"
    elif any(kw in prompt_lower for kw in ["用户", "user"]):
        return "user-management"
    else:
        return "general"


def main():
    """
    主函数：处理 PostToolUse Hook 输入。
    
    Claude Code Hook 传递 JSON 格式数据到 stdin。
    """
    try:
        # 读取 Hook 输入
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        # 无有效输入，跳过
        sys.exit(0)
    
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    
    # 只处理 Task 工具
    if tool_name != "Task":
        sys.exit(0)
    
    # 提取关键信息
    agent_type = tool_input.get("agent", "unknown")
    prompt = tool_input.get("prompt", "")
    result = tool_response.get("result", "")
    
    # 计算奖励分数
    reward = calculate_reward(agent_type, prompt, result)
    
    # 存储到经验池
    save_experience(agent_type, prompt, reward, result)
    
    # 输出结果（供调试）
    output = {
        "agent": agent_type,
        "reward": reward,
        "action": "stored",
        "timestamp": datetime.now().isoformat()
    }
    
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
