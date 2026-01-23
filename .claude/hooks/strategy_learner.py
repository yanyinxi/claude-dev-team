#!/usr/bin/env python3
"""
策略学习器 (Strategy Learner)

职责：
1. 监听 SubagentStop 事件（子代理执行完成）
2. 分析策略效果，提取洞察
3. 去重检查（24小时内相同策略不重复）
4. 经验聚合（多条相似经验合并为一条）
5. 实时写入 .claude/rules/*.md

使用 Claude Code 原生 Hook 机制实现，0% 重复造轮子。
"""

import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Optional, List, Dict, Any


def should_update_rules(agent_type: str, strategy_keyword: str, time_window_hours: int = 24) -> bool:
    """
    检查是否需要更新规则。
    
    去重机制：相同策略在24小时内不重复更新，避免刷屏。
    
    Args:
        agent_type: Agent 类型 (frontend-developer, backend-developer 等)
        strategy_keyword: 策略关键词 (frontend, backend, testing 等)
        time_window_hours: 时间窗口（默认24小时）
    
    Returns:
        True: 需要更新
        False: 已在近期更新过，跳过
    """
    rules_file = Path(f".claude/rules/{agent_type.split('-')[0]}.md")
    
    # 文件不存在，需要创建
    if not rules_file.exists():
        return True
    
    try:
        content = rules_file.read_text(encoding='utf-8')
    except IOError:
        return True
    
    # 查找最近的更新时间
    time_pattern = r"更新时间:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
    matches = list(re.finditer(time_pattern, content))
    
    if not matches:
        return True  # 没有更新时间记录，需要更新
    
    # 获取最近更新时间
    last_match = matches[-1]
    try:
        last_time = datetime.fromisoformat(last_match.group(1))
    except ValueError:
        return True
    
    now = datetime.now()
    hours_since_update = (now - last_time).total_seconds() / 3600
    
    # 24小时内检查策略关键词是否相同
    if hours_since_update < time_window_hours:
        # 检查是否有相同策略关键词的更新记录
        keyword_pattern = rf"策略关键词:.*{strategy_keyword}"
        if re.search(keyword_pattern, content, re.DOTALL | re.IGNORECASE):
            return False  # 24小时内相同策略，跳过
    
    return True


def aggregate_experiences(experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    聚合多条相似经验为一条。
    
    聚合机制：
    - 连续2次以上相同策略类型 → 合并为一条聚合经验
    - 计算平均奖励分数
    - 合并描述信息
    
    Args:
        experiences: 原始经验列表（从 experience_pool.json 读取）
    
    Returns:
        聚合后的经验列表
    """
    if not experiences:
        return []
    
    if len(experiences) < 2:
        return experiences
    
    # 按策略关键词分组
    by_keyword = defaultdict(list)
    
    for exp in experiences:
        keyword = exp.get("strategy_keyword", "general")
        by_keyword[keyword].append(exp)
    
    aggregated = []
    
    for keyword, group in by_keyword.items():
        if len(group) >= 2:
            # 计算平均奖励
            rewards = [e.get("reward", 0) for e in group]
            avg_reward = sum(rewards) / len(rewards) if rewards else 0
            
            # 合并描述（去重）
            descriptions = set()
            for e in group:
                preview = e.get("result_preview", "")
                if preview:
                    descriptions.add(preview[:100])
            
            merged_description = " | ".join(descriptions) if descriptions else ""
            
            aggregated.append({
                "strategy_keyword": keyword,
                "description": merged_description,
                "reward": round(avg_reward, 2),
                "count": len(group),  # 聚合次数
                "is_aggregated": True,
                "timestamp": datetime.now().isoformat()
            })
        else:
            # 单次经验直接添加
            group[0]["is_aggregated"] = False
            aggregated.append(group[0])
    
    # 只保留最近5条
    return aggregated[-5:]


def analyze_strategy(agent_type: str, result: str) -> List[Dict[str, Any]]:
    """
    分析策略执行结果，提取洞察。
    
    Args:
        agent_type: Agent 类型
        result: 执行结果文本
    
    Returns:
        洞察列表
    """
    insights = []
    
    # 提取最佳实践
    if "最佳实践" in result:
        # 尝试提取最佳实践描述
        parts = result.split("最佳实践")
        for part in parts[1:]:
            # 找到冒号后的内容
            if ":" in part:
                practice = part.split(":")[1].strip().split("\n")[0]
                insights.append({
                    "category": "best_practice",
                    "description": practice,
                    "agent": agent_type
                })
    
    # 提取改进建议
    if any(kw in result for kw in ["需要改进", "教训", "问题", "不足"]):
        parts = result.split("\n")
        for part in parts:
            if any(kw in part for kw in ["需要改进", "教训"]):
                if ":" in part:
                    improvement = part.split(":")[1].strip()
                    insights.append({
                        "category": "improvement",
                        "description": improvement,
                        "agent": agent_type
                    })
    
    # 提取协作洞察
    if any(kw in result for kw in ["协作", "配合", "沟通"]):
        insights.append({
            "category": "collaboration",
            "description": "团队协作顺畅，配合默契",
            "agent": agent_type
        })
    
    # 提取效率洞察
    if any(kw in result for kw in ["效率", "快速", "按时"]):
        insights.append({
            "category": "efficiency",
            "description": "任务执行效率高",
            "agent": agent_type
        })
    
    return insights


def format_rule_content(agent_category: str, strategy_keyword: str, 
                        insights: List[Dict[str, Any]], 
                        aggregated: List[Dict[str, Any]] = None) -> str:
    """
    格式化规则文件内容。
    
    Args:
        agent_category: Agent 类别 (frontend, backend 等)
        strategy_keyword: 策略关键词
        insights: 洞察列表
        aggregated: 聚合经验列表
    
    Returns:
        格式化的规则内容
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"""---
paths: ""
---

# {agent_category.title()} Strategy Rules

**更新时间**: {timestamp}
**策略关键词**: {strategy_keyword}

## 新学到的洞察

"""
    # 添加实时洞察
    if insights:
        for insight in insights:
            category_emoji = {
                "best_practice": "✅",
                "improvement": "⚠️",
                "collaboration": "🤝",
                "efficiency": "⚡"
            }.get(insight.get("category", ""), "📝")
            
            content += f"""### {category_emoji} {insight.get('category', '经验').title()}

- **Agent**: {insight.get('agent', agent_category)}
- **描述**: {insight.get('description', '无')}

"""
    
    # 添加聚合经验
    if aggregated:
        content += "\n## 聚合经验 (基于多次执行)\n\n"
        
        for exp in aggregated:
            if exp.get("is_aggregated"):
                content += f"""### 📊 聚合洞察 (基于 {exp.get('count', 1)} 次执行)

- **平均奖励**: {exp.get('reward', 0)}/10
- **策略**: {exp.get('strategy_keyword', 'general')}
- **描述**: {exp.get('description', '无')}

"""
    
    return content


def update_rules_file(agent_type: str, strategy_keyword: str, 
                      insights: List[Dict[str, Any]], 
                      aggregated: List[Dict[str, Any]] = None) -> bool:
    """
    更新规则文件。
    
    Args:
        agent_type: Agent 类型
        strategy_keyword: 策略关键词
        insights: 洞察列表
        aggregated: 聚合经验
    
    Returns:
        是否更新成功
    """
    # 获取 Agent 类别（去掉 "-developer" 后缀）
    agent_category = agent_type.replace("-developer", "").replace("-reviewer", "").replace("-lead", "")
    
    rules_dir = Path(".claude/rules")
    rules_dir.mkdir(exist_ok=True)
    
    rules_file = rules_dir / f"{agent_category}.md"
    
    # 生成新内容
    new_content = format_rule_content(agent_category, strategy_keyword, insights, aggregated)
    
    try:
        if rules_file.exists():
            # 读取现有内容
            existing_content = rules_file.read_text(encoding='utf-8')

            # 检查是否需要追加（去重逻辑）
            if not should_update_rules(agent_type, strategy_keyword, 24):
                print(json.dumps({
                    "action": "skipped",
                    "reason": "相同策略最近已更新",
                    "agent": agent_type
                }, ensure_ascii=False))
                return False

            # 追加新内容（保留原有内容）
            # 只保留第一个 frontmatter 和标题，追加新的洞察
            if "## 新学到的洞察" in existing_content:
                # 找到第一个 "## 新学到的洞察" 的位置
                parts = existing_content.split("## 新学到的洞察", 1)
                # 只保留第一个 frontmatter 和标题部分
                header = parts[0]
                # 移除多余的 frontmatter（保留第一个）
                if header.count("---") > 2:
                    # 找到第一个完整的 frontmatter
                    first_end = header.find("---", 3)
                    if first_end != -1:
                        header = header[:first_end + 3] + "\n\n" + "# " + agent_category.title() + " Strategy Rules\n\n"
                        header += f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                        header += f"**策略关键词**: {strategy_keyword}\n\n"

                # 提取新内容的洞察部分（不包含 frontmatter 和标题）
                new_insights = new_content.split("## 新学到的洞察", 1)[1] if "## 新学到的洞察" in new_content else ""
                combined_content = header + "## 新学到的洞察" + new_insights
            else:
                combined_content = existing_content + "\n\n" + new_content

            rules_file.write_text(combined_content, encoding='utf-8')
        else:
            # 新建文件
            rules_file.write_text(new_content, encoding='utf-8')
        
        return True
        
    except IOError as e:
        print(json.dumps({
            "action": "error",
            "message": str(e)
        }, ensure_ascii=False))
        return False


def load_experience_pool() -> List[Dict[str, Any]]:
    """
    加载经验池数据。
    
    Returns:
        经验列表
    """
    experience_file = Path(".claude/experience_pool.json")
    
    if not experience_file.exists():
        return []
    
    try:
        with open(experience_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def main():
    """
    主函数：处理 SubagentStop Hook 输入。
    
    Claude Code Hook 传递 JSON 格式数据到 stdin。
    """
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)
    
    # 提取关键信息
    agent_type = input_data.get("agent_type", input_data.get("agent", "unknown"))
    result = input_data.get("result", "")
    
    # 推断策略关键词
    strategy_keyword = infer_strategy_keyword(result)
    
    # 分析策略洞察
    insights = analyze_strategy(agent_type, result)
    
    # 加载并聚合经验
    experiences = load_experience_pool()
    agent_experiences = [e for e in experiences if e.get("agent") == agent_type]
    aggregated = aggregate_experiences(agent_experiences)
    
    # 更新规则文件
    success = update_rules_file(agent_type, strategy_keyword, insights, aggregated)
    
    # 输出结果
    output = {
        "agent": agent_type,
        "strategy_keyword": strategy_keyword,
        "insights_count": len(insights),
        "aggregated_count": len(aggregated) if aggregated else 0,
        "action": "updated" if success else "skipped",
        "timestamp": datetime.now().isoformat()
    }
    
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


def infer_strategy_keyword(text: str) -> str:
    """
    从文本推断策略关键词。
    
    Args:
        text: 文本内容
    
    Returns:
        策略关键词
    """
    text_lower = text.lower()
    
    if any(kw in text_lower for kw in ["前端", "ui", "组件", "frontend", "react"]):
        return "frontend"
    elif any(kw in text_lower for kw in ["后端", "api", "数据库", "backend", "server"]):
        return "backend"
    elif any(kw in text_lower for kw in ["测试", "test", "验证"]):
        return "testing"
    elif any(kw in text_lower for kw in ["架构", "设计", "architecture", "design"]):
        return "architecture"
    elif any(kw in text_lower for kw in ["产品", "需求", "product", "prd"]):
        return "product"
    elif any(kw in text_lower for kw in ["审查", "review", "代码质量"]):
        return "review"
    else:
        return "general"


if __name__ == "__main__":
    main()
