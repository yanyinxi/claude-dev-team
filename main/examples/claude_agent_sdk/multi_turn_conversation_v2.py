#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================
Claude SDK 多轮对话示例 V2 (优化版)
=====================================================
功能：演示如何使用 Claude SDK 进行多轮对话
作者：Claude Dev Team
创建时间：2026-01-30
版本：2.0

本示例演示：
1. 维护对话历史
2. 保持上下文连贯性
3. 交互式对话循环
4. 对话历史管理
5. 流式输出（可选）
6. 智能意图推荐（带缓存）
7. 需求澄清（多轮支持）
8. 对话摘要和压缩
9. 错误重试机制
10. 完善的日志记录
=====================================================
"""

import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 导入配置模块
import config

# =====================================================
# 配置日志
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("conversation.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# =====================================================
# 数据类定义
# =====================================================


class CommandType(Enum):
    """命令类型枚举"""

    QUIT = "quit"
    EXIT = "exit"
    CLEAR = "clear"
    SAVE = "save"
    HELP = "help"
    HISTORY = "history"
    SUMMARY = "summary"
    STATS = "stats"


@dataclass
class ConversationConfig:
    """对话配置"""

    max_history: int = 20  # 最大保留的对话轮数
    max_input_length: int = 2000  # 最大输入长度
    enable_streaming: bool = True  # 是否启用流式输出
    enable_intent_recommendation: bool = True  # 是否启用意图推荐
    enable_clarification: bool = True  # 是否启用需求澄清
    intent_cache_ttl: int = 300  # 意图推荐缓存时间（秒）
    max_retries: int = 3  # 最大重试次数
    retry_delay: float = 1.0  # 重试延迟（秒）


@dataclass
class IntentRecommendation:
    """意图推荐"""

    recommendations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    is_cached: bool = False


# =====================================================
# 增强的对话管理类
# =====================================================


class EnhancedConversationManager:
    """
    增强的对话管理器

    新增功能：
    - 对话摘要
    - 上下文压缩
    - 意图推荐缓存
    - 统计信息
    - 日志记录
    """

    def __init__(self, config: ConversationConfig = None):
        """
        初始化对话管理器

        Args:
            config: 对话配置
        """
        self.config = config or ConversationConfig()
        self.messages: List[Dict[str, str]] = []
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.intent_cache: Optional[IntentRecommendation] = None
        self.stats = {
            "total_turns": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0,
            "start_time": time.time(),
        }
        logger.info(f"对话管理器已初始化，ID: {self.conversation_id}")

    def add_user_message(self, content: str) -> bool:
        """
        添加用户消息

        Args:
            content: 消息内容

        Returns:
            是否添加成功
        """
        if len(content) > self.config.max_input_length:
            logger.warning(f"用户输入过长: {len(content)} 字符")
            return False

        self.messages.append({"role": "user", "content": content})
        self._trim_history()
        self._invalidate_intent_cache()
        logger.debug(f"添加用户消息: {content[:50]}...")
        return True

    def add_assistant_message(self, content: str):
        """添加助手消息"""
        self.messages.append({"role": "assistant", "content": content})
        self._trim_history()
        self.stats["total_turns"] += 1
        logger.debug(f"添加助手消息: {content[:50]}...")

    def _trim_history(self):
        """
        修剪对话历史

        保留最近的 max_history 轮对话
        """
        if len(self.messages) > self.config.max_history * 2:
            removed_count = len(self.messages) - self.config.max_history * 2
            self.messages = self.messages[-(self.config.max_history * 2) :]
            logger.info(f"修剪对话历史，移除 {removed_count} 条消息")

    def _invalidate_intent_cache(self):
        """使意图推荐缓存失效"""
        self.intent_cache = None

    def get_messages(self) -> List[Dict[str, str]]:
        """获取所有消息"""
        return self.messages

    def get_message_count(self) -> int:
        """获取消息数量"""
        return len(self.messages)

    def get_turn_count(self) -> int:
        """获取对话轮数"""
        return self.stats["total_turns"]

    def update_stats(self, input_tokens: int, output_tokens: int):
        """
        更新统计信息

        Args:
            input_tokens: 输入 token 数
            output_tokens: 输出 token 数
        """
        self.stats["total_input_tokens"] += input_tokens
        self.stats["total_output_tokens"] += output_tokens
        # 简化的成本计算（实际成本取决于模型）
        self.stats["total_cost"] += (input_tokens * 0.003 + output_tokens * 0.015) / 1000

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        duration = time.time() - self.stats["start_time"]
        return {
            **self.stats,
            "duration_seconds": duration,
            "avg_tokens_per_turn": (
                (self.stats["total_input_tokens"] + self.stats["total_output_tokens"])
                / max(self.stats["total_turns"], 1)
            ),
        }

    def clear(self):
        """清空对话历史"""
        self.messages = []
        self._invalidate_intent_cache()
        logger.info("对话历史已清空")

    def save_to_file(self, filename: str = None):
        """
        保存对话到文件

        Args:
            filename: 文件名（可选）
        """
        if filename is None:
            filename = f"conversation_{self.conversation_id}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"对话 ID: {self.conversation_id}\n")
                f.write(f"对话时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"消息数量: {len(self.messages)}\n")
                f.write(f"对话轮数: {self.stats['total_turns']}\n")
                f.write(f"总 Tokens: {self.stats['total_input_tokens'] + self.stats['total_output_tokens']}\n")
                f.write(f"预估成本: ${self.stats['total_cost']:.4f}\n")
                f.write("=" * 60 + "\n\n")

                for i, msg in enumerate(self.messages, 1):
                    role = "👤 用户" if msg["role"] == "user" else "🤖 Claude"
                    f.write(f"[{i}] {role}:\n{msg['content']}\n\n")

            logger.info(f"对话已保存到: {filename}")
            print(f"✅ 对话已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存对话失败: {str(e)}")
            print(f"❌ 保存失败: {str(e)}")

    def get_summary(self, client) -> str:
        """
        生成对话摘要

        Args:
            client: Claude 客户端

        Returns:
            对话摘要
        """
        if len(self.messages) < 2:
            return "对话内容过少，无法生成摘要"

        try:
            # 构建摘要 prompt
            conversation_text = "\n".join(
                [f"{msg['role']}: {msg['content'][:200]}" for msg in self.messages]
            )

            prompt = f"""请用 2-3 句话总结以下对话的主要内容：

{conversation_text}

摘要："""

            response = client.messages.create(
                model=config.DEFAULT_MODEL,
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )

            summary = response.content[0].text.strip()
            logger.info(f"生成对话摘要: {summary[:50]}...")
            return summary

        except Exception as e:
            logger.error(f"生成摘要失败: {str(e)}")
            return f"生成摘要失败: {str(e)}"


# =====================================================
# 增强的交互式对话助手
# =====================================================


class InteractiveConversationAssistant:
    """
    交互式对话助手

    新增功能：
    - 流式输出
    - 智能意图推荐（带缓存）
    - 多轮需求澄清
    - 错误重试
    - 快捷命令
    """

    def __init__(self, client, config: ConversationConfig = None):
        """
        初始化对话助手

        Args:
            client: Claude 客户端
            config: 对话配置
        """
        self.client = client
        self.config = config or ConversationConfig()
        self.conversation = EnhancedConversationManager(config)
        logger.info("交互式对话助手已初始化")

    def generate_intent_recommendations(self) -> List[str]:
        """
        生成用户意图推荐（带缓存）

        Returns:
            推荐的用户意图列表（最多 3 个）
        """
        # 检查缓存
        if self.conversation.intent_cache:
            cache_age = time.time() - self.conversation.intent_cache.timestamp
            if cache_age < self.config.intent_cache_ttl:
                logger.debug("使用缓存的意图推荐")
                return self.conversation.intent_cache.recommendations

        messages = self.conversation.get_messages()
        if len(messages) < 2:
            return []

        try:
            # 构建 prompt（使用最近 6 条消息）
            recent_messages = messages[-6:]
            conversation_text = "\n".join(
                [
                    f"{'用户' if msg['role'] == 'user' else 'Claude'}: {msg['content'][:200]}"
                    for msg in recent_messages
                ]
            )

            prompt = f"""基于以下对话历史，推荐 3 个用户可能想继续询问的问题。

对话历史：
{conversation_text}

要求：
1. 每行一个问题
2. 简洁明了（不超过 20 字）
3. 与对话主题相关
4. 不需要编号

推荐问题："""

            response = self.client.messages.create(
                model=config.DEFAULT_MODEL,
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )

            recommendations_text = response.content[0].text.strip()
            recommendations = [
                r.strip().lstrip("0123456789.。 ")
                for r in recommendations_text.split("\n")
                if r.strip()
            ]
            recommendations = recommendations[:3]

            # 更新缓存
            self.conversation.intent_cache = IntentRecommendation(
                recommendations=recommendations, timestamp=time.time(), is_cached=False
            )

            logger.info(f"生成意图推荐: {recommendations}")
            return recommendations

        except Exception as e:
            logger.error(f"生成意图推荐失败: {str(e)}")
            return []

    def check_clarification_needed(self, user_input: str) -> Optional[str]:
        """
        检查用户输入是否需要需求澄清（支持多轮）

        Args:
            user_input: 用户输入

        Returns:
            澄清问题（如果没有则返回 None）
        """
        if not self.config.enable_clarification:
            return None

        # 检测模糊关键词
        vague_keywords = ["一些", "某个", "随便", "大概", "可能", "相关", "有关", "什么", "怎么"]
        if any(kw in user_input for kw in vague_keywords):
            if len(user_input) < 15:
                return "为了更好地帮助您，能否详细说明一下您的具体需求？"

        # 检测过短输入
        if len(user_input) < 5:
            return "您能提供更多细节吗？这样我可以给出更准确的回答。"

        return None

    def send_message_with_retry(
        self, user_input: str, use_streaming: bool = None
    ) -> Tuple[Optional[str], Optional[Dict[str, int]]]:
        """
        发送消息并支持重试

        Args:
            user_input: 用户输入
            use_streaming: 是否使用流式输出（None 表示使用配置）

        Returns:
            (助手回复, 使用统计) 或 (None, None) 如果失败
        """
        if use_streaming is None:
            use_streaming = self.config.enable_streaming

        for attempt in range(self.config.max_retries):
            try:
                if use_streaming:
                    return self._send_streaming_message()
                else:
                    return self._send_normal_message()

            except Exception as e:
                logger.warning(f"发送消息失败 (尝试 {attempt + 1}/{self.config.max_retries}): {str(e)}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    logger.error(f"发送消息失败，已达最大重试次数: {str(e)}")
                    return None, None

    def _send_normal_message(self) -> Tuple[str, Dict[str, int]]:
        """发送普通消息"""
        response = self.client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=2048,
            messages=self.conversation.get_messages(),
        )

        assistant_message = response.content[0].text
        usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}

        return assistant_message, usage

    def _send_streaming_message(self) -> Tuple[str, Dict[str, int]]:
        """发送流式消息"""
        print("\n🤖 Claude:")
        full_response = ""

        with self.client.messages.stream(
            model=config.DEFAULT_MODEL,
            max_tokens=2048,
            messages=self.conversation.get_messages(),
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

        print()  # 换行

        # 获取使用统计
        final_message = stream.get_final_message()
        usage = {
            "input_tokens": final_message.usage.input_tokens,
            "output_tokens": final_message.usage.output_tokens,
        }

        return full_response, usage

    def handle_command(self, command: str) -> bool:
        """
        处理特殊命令

        Args:
            command: 命令字符串

        Returns:
            是否应该退出对话
        """
        command_lower = command.lower().strip()

        # 退出命令
        if command_lower in ["quit", "exit", "q"]:
            print("\n👋 再见！对话已结束。")
            return True

        # 清空历史
        if command_lower == "clear":
            self.conversation.clear()
            print("✅ 对话历史已清空")
            return False

        # 保存对话
        if command_lower == "save":
            self.conversation.save_to_file()
            return False

        # 显示帮助
        if command_lower == "help":
            self.show_help()
            return False

        # 显示历史
        if command_lower == "history":
            self.show_history()
            return False

        # 显示摘要
        if command_lower == "summary":
            summary = self.conversation.get_summary(self.client)
            print(f"\n📝 对话摘要:\n{summary}")
            return False

        # 显示统计
        if command_lower == "stats":
            self.show_stats()
            return False

        return False

    def show_help(self):
        """显示帮助信息"""
        print("\n" + "=" * 60)
        print("📖 可用命令")
        print("=" * 60)
        print("  quit/exit/q  - 退出对话")
        print("  clear        - 清空对话历史")
        print("  save         - 保存对话到文件")
        print("  help         - 显示此帮助信息")
        print("  history      - 显示对话历史")
        print("  summary      - 生成对话摘要")
        print("  stats        - 显示统计信息")
        print("=" * 60)

    def show_history(self):
        """显示对话历史"""
        messages = self.conversation.get_messages()
        if not messages:
            print("\n⚠️ 对话历史为空")
            return

        print("\n" + "=" * 60)
        print("📜 对话历史")
        print("=" * 60)
        for i, msg in enumerate(messages, 1):
            role = "👤 用户" if msg["role"] == "user" else "🤖 Claude"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"[{i}] {role}: {content}")
        print("=" * 60)

    def show_stats(self):
        """显示统计信息"""
        stats = self.conversation.get_stats()
        print("\n" + "=" * 60)
        print("📊 对话统计")
        print("=" * 60)
        print(f"对话轮数: {stats['total_turns']}")
        print(f"消息数量: {self.conversation.get_message_count()}")
        print(f"输入 Tokens: {stats['total_input_tokens']}")
        print(f"输出 Tokens: {stats['total_output_tokens']}")
        print(f"总 Tokens: {stats['total_input_tokens'] + stats['total_output_tokens']}")
        print(f"平均 Tokens/轮: {stats['avg_tokens_per_turn']:.1f}")
        print(f"对话时长: {stats['duration_seconds']:.1f} 秒")
        print(f"预估成本: ${stats['total_cost']:.4f}")
        print("=" * 60)

    def run(self):
        """运行交互式对话循环"""
        print("\n" + "=" * 60)
        print("🤖 Claude 助手已启动！")
        print("=" * 60)
        print("💡 提示：输入 'help' 查看可用命令")
        print("=" * 60)

        while True:
            try:
                # 获取用户输入
                turn_num = self.conversation.get_turn_count() + 1
                print(f"\n👤 用户 (第 {turn_num} 轮):")
                user_input = input("> ").strip()

                # 处理空输入
                if not user_input:
                    print("⚠️ 请输入内容")
                    continue

                # 处理特殊命令
                if self.handle_command(user_input):
                    break

                # 验证输入长度
                if len(user_input) > self.config.max_input_length:
                    print(f"⚠️ 输入过长（最大 {self.config.max_input_length} 字符）")
                    continue

                # 检查是否需要需求澄清
                clarification = self.check_clarification_needed(user_input)
                if clarification:
                    print(f"\n💡 需求澄清建议: {clarification}")

                # 添加用户消息
                if not self.conversation.add_user_message(user_input):
                    print("❌ 添加消息失败")
                    continue

                # 发送消息并获取回复
                print("\n🤖 Claude 正在思考...")
                assistant_message, usage = self.send_message_with_retry(user_input)

                if assistant_message is None:
                    print("❌ 获取回复失败，请重试")
                    self.conversation.messages.pop()  # 移除用户消息
                    continue

                # 添加助手消息
                self.conversation.add_assistant_message(assistant_message)

                # 更新统计
                if usage:
                    self.conversation.update_stats(usage["input_tokens"], usage["output_tokens"])

                # 如果不是流式输出，显示回复
                if not self.config.enable_streaming:
                    print(f"\n🤖 Claude:\n{assistant_message}")

                # 生成并显示意图推荐
                if self.config.enable_intent_recommendation:
                    recommendations = self.generate_intent_recommendations()
                    if recommendations:
                        print("\n📌 推荐下一步操作：")
                        for i, rec in enumerate(recommendations, 1):
                            print(f"   {i}. {rec}")

                # 显示简要统计
                if usage:
                    print(
                        f"\n📊 [轮数: {self.conversation.get_turn_count()} | "
                        f"消息: {self.conversation.get_message_count()} | "
                        f"Tokens: {usage['input_tokens']}→{usage['output_tokens']}]"
                    )

            except KeyboardInterrupt:
                print("\n\n⚠️ 用户中断")
                break
            except Exception as e:
                logger.error(f"运行时错误: {str(e)}")
                print(f"\n❌ 错误: {str(e)}")

        # 对话结束后，询问是否保存
        if self.conversation.get_message_count() > 0:
            save_choice = input("\n💾 是否保存对话？(y/n): ").strip().lower()
            if save_choice == "y":
                self.conversation.save_to_file()

        # 显示最终统计
        self.show_stats()


# =====================================================
# 示例函数
# =====================================================


def example_2_interactive_conversation_v2():
    """
    示例 2：交互式对话循环（优化版）

    新增功能：
    - 流式输出
    - 智能意图推荐（带缓存）
    - 多轮需求澄清
    - 错误重试机制
    - 快捷命令（help, history, summary, stats）
    - 对话摘要
    - 完善的统计信息
    - 日志记录
    """
    print("\n" + "=" * 60)
    print("示例 2：交互式对话循环（优化版 V2）")
    print("=" * 60)

    try:
        # 创建客户端
        client = config.create_client()
        if not client:
            return

        # 创建配置
        conv_config = ConversationConfig(
            max_history=10,
            enable_streaming=True,
            enable_intent_recommendation=True,
            enable_clarification=True,
            max_retries=3,
        )

        # 创建对话助手
        assistant = InteractiveConversationAssistant(client, conv_config)

        # 运行对话循环
        assistant.run()

        print("\n✅ 示例 2 完成")

    except Exception as e:
        logger.error(f"示例运行失败: {str(e)}")
        print(f"❌ 错误: {str(e)}")


# =====================================================
# 主函数
# =====================================================


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Claude SDK 多轮对话示例 V2（优化版）")
    print("=" * 60)

    # 验证配置
    is_valid, error_msg = config.validate_config()
    if not is_valid:
        print(f"\n❌ 错误：{error_msg}")
        print("\n请先设置 API Key：")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        return

    print("\n✅ API Key 已配置")

    # 运行优化版示例
    example_2_interactive_conversation_v2()


if __name__ == "__main__":
    main()
