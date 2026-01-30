#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================
Claude SDK 多轮对话示例
=====================================================
功能：演示如何使用 Claude SDK 进行多轮对话
作者：Claude Dev Team
创建时间：2026-01-25

本示例演示：
1. 维护对话历史
2. 保持上下文连贯性
3. 交互式对话循环
4. 对话历史管理
5. 流式输出（可选）
=====================================================
"""

import os
import sys
from typing import List, Dict, Any
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 导入配置模块
import config


# =====================================================
# 多轮对话管理类
# =====================================================


class ConversationManager:
    """
    对话管理器

    功能：
    - 维护对话历史
    - 管理上下文
    - 控制对话长度
    - 保存和加载对话
    """

    def __init__(self, max_history: int = 20):
        """
        初始化对话管理器

        Args:
            max_history: 最大保留的对话轮数（防止上下文过长）
        """
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def add_user_message(self, content: str):
        """添加用户消息"""
        self.messages.append({"role": "user", "content": content})
        self._trim_history()

    def add_assistant_message(self, content: str):
        """添加助手消息"""
        self.messages.append({"role": "assistant", "content": content})
        self._trim_history()

    def _trim_history(self):
        """
        修剪对话历史

        保留最近的 max_history 轮对话
        注意：一轮对话 = 1 个用户消息 + 1 个助手消息
        """
        if len(self.messages) > self.max_history * 2:
            # 保留最近的消息
            self.messages = self.messages[-(self.max_history * 2) :]

    def get_messages(self) -> List[Dict[str, str]]:
        """获取所有消息"""
        return self.messages

    def get_message_count(self) -> int:
        """获取消息数量"""
        return len(self.messages)

    def clear(self):
        """清空对话历史"""
        self.messages = []

    def save_to_file(self, filename: str = None):
        """
        保存对话到文件

        Args:
            filename: 文件名（可选，默认使用时间戳）
        """
        if filename is None:
            filename = f"conversation_{self.conversation_id}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"对话 ID: {self.conversation_id}\n")
            f.write(f"对话时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"消息数量: {len(self.messages)}\n")
            f.write("=" * 60 + "\n\n")

            for i, msg in enumerate(self.messages, 1):
                role = "👤 用户" if msg["role"] == "user" else "🤖 Claude"
                f.write(f"[{i}] {role}:\n{msg['content']}\n\n")

        print(f"✅ 对话已保存到: {filename}")


# =====================================================
# 示例 1：基础多轮对话
# =====================================================


def example_1_basic_multi_turn():
    """
    示例 1：基础多轮对话

    演示如何进行简单的多轮对话
    """
    print("\n" + "=" * 60)
    print("示例 1：基础多轮对话")
    print("=" * 60)

    try:
        # 创建客户端和对话管理器
        client = config.create_client()
        if not client:
            return

        conversation = ConversationManager()

        print("\n开始多轮对话演示...")

        # 第 1 轮对话
        print("\n" + "-" * 60)
        print("🗣️ 第 1 轮对话")
        print("-" * 60)

        user_msg_1 = "你好！我想学习 Python 编程，你能推荐一些学习资源吗？"
        print(f"👤 用户: {user_msg_1}")
        conversation.add_user_message(user_msg_1)

        response_1 = client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            messages=conversation.get_messages(),
        )

        assistant_msg_1 = response_1.content[0].text
        print(f"\n🤖 Claude: {assistant_msg_1}")
        conversation.add_assistant_message(assistant_msg_1)

        # 第 2 轮对话（基于上一轮的上下文）
        print("\n" + "-" * 60)
        print("🗣️ 第 2 轮对话")
        print("-" * 60)

        user_msg_2 = "这些资源中，哪个最适合完全没有编程基础的初学者？"
        print(f"👤 用户: {user_msg_2}")
        conversation.add_user_message(user_msg_2)

        response_2 = client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            messages=conversation.get_messages(),
        )

        assistant_msg_2 = response_2.content[0].text
        print(f"\n🤖 Claude: {assistant_msg_2}")
        conversation.add_assistant_message(assistant_msg_2)

        # 第 3 轮对话（继续深入）
        print("\n" + "-" * 60)
        print("🗣️ 第 3 轮对话")
        print("-" * 60)

        user_msg_3 = "学完基础后，我应该做什么项目来练习？"
        print(f"👤 用户: {user_msg_3}")
        conversation.add_user_message(user_msg_3)

        response_3 = client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            messages=conversation.get_messages(),
        )

        assistant_msg_3 = response_3.content[0].text
        print(f"\n🤖 Claude: {assistant_msg_3}")
        conversation.add_assistant_message(assistant_msg_3)

        # 显示对话统计
        print("\n" + "=" * 60)
        print("📊 对话统计")
        print("=" * 60)
        print(f"总消息数: {conversation.get_message_count()}")
        print(f"对话轮数: {conversation.get_message_count() // 2}")

        # 保存对话
        conversation.save_to_file()

        print("\n✅ 示例 1 完成")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")


# =====================================================
# 示例 2：交互式对话循环
# =====================================================


def example_2_interactive_conversation():
    """
    示例 2：交互式对话循环

    演示如何创建一个交互式的对话循环
    用户可以持续输入，直到输入 'quit' 退出

    新增功能：
    - 需求澄清：根据用户输入，主动识别信息缺失并询问
    - 意图推荐：基于对话历史，推荐 3 个可能的用户意图
    """
    print("\n" + "=" * 60)
    print("示例 2：交互式对话循环")
    print("=" * 60)

    try:
        # 创建客户端和对话管理器
        client = config.create_client()
        if not client:
            return

        conversation = ConversationManager(max_history=10)

        print("\n🤖 Claude 助手已启动！")
        print("💡 提示：输入 'quit' 或 'exit' 退出对话")
        print("💡 提示：输入 'clear' 清空对话历史")
        print("💡 提示：输入 'save' 保存对话到文件")
        print("=" * 60)

        turn_count = 0

        def generate_intent_recommendations(
            conversation: ConversationManager,
        ) -> List[str]:
            """
            基于对话历史生成用户意图推荐

            Args:
                conversation: 对话管理器

            Returns:
                推荐的用户意图列表（最多 3 个）
            """
            messages = conversation.get_messages()
            if len(messages) < 2:
                return []

            try:
                prompt = """基于以下对话历史，推荐 3 个用户可能想继续询问的问题（只需返回问题列表，每行一个，不需要编号）：对话历史："""
                for msg in messages[-6:]:
                    role = "用户" if msg["role"] == "user" else "Claude"
                    prompt += f"{role}: {msg['content'][:200]}\n"

                prompt += """ 请推荐 3 个用户可能想问的后续问题（每行一个，简洁明了）："""

                response = client.messages.create(
                    model=config.DEFAULT_MODEL,
                    max_tokens=256,
                    messages=[{"role": "user", "content": prompt}],
                )

                recommendations = response.content[0].text.strip().split("\n")
                recommendations = [
                    r.strip().lstrip("0123456789.。 ")
                    for r in recommendations
                    if r.strip()
                ]
                return recommendations[:3]

            except Exception:
                return []

        def check_clarification_needed(
            user_input: str, conversation: ConversationManager
        ) -> str:
            """
            检查用户输入是否需要需求澄清

            Args:
                user_input: 用户输入
                conversation: 对话管理器

            Returns:
                澄清问题（如果没有则返回空字符串）
            """
            if len(conversation.get_messages()) > 0:
                return ""

            vague_keywords = ["一些", "某个", "随便", "大概", "可能", "相关", "有关"]
            if any(kw in user_input for kw in vague_keywords):
                return "为了更好地帮助您，能否详细说明一下您的具体需求？"

            if len(user_input) < 10:
                return "您能提供更多细节吗？这样我可以给出更准确的回答。"

            return ""

        while True:
            # 获取用户输入
            print(f"\n👤 用户 (第 {turn_count + 1} 轮):")
            user_input = input("> ").strip()

            # 处理特殊命令
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 再见！对话已结束。")
                break

            if user_input.lower() == "clear":
                conversation.clear()
                print("✅ 对话历史已清空")
                turn_count = 0
                continue

            if user_input.lower() == "save":
                conversation.save_to_file()
                continue

            if not user_input:
                print("⚠️ 请输入内容")
                continue

            # 检查是否需要需求澄清
            clarification = check_clarification_needed(user_input, conversation)
            if clarification:
                print(f"\n💡 需求澄清建议: {clarification}")

            # 添加用户消息
            conversation.add_user_message(user_input)

            try:
                # 发送请求到 Claude
                print("\n🤖 Claude 正在思考...")
                response = client.messages.create(
                    model=config.DEFAULT_MODEL,
                    max_tokens=2048,
                    messages=conversation.get_messages(),
                )

                # 获取回复
                assistant_message = response.content[0].text
                conversation.add_assistant_message(assistant_message)

                # 显示回复
                print(f"\n🤖 Claude:")
                print(assistant_message)

                # 生成并显示意图推荐
                recommendations = generate_intent_recommendations(conversation)
                if recommendations:
                    print("\n📌 推荐下一步操作：")
                    for i, rec in enumerate(recommendations, 1):
                        print(f"   {i}. {rec}")

                # 显示统计信息
                turn_count += 1
                print(
                    f"\n📊 [对话轮数: {turn_count} | 消息数: {conversation.get_message_count()} | Tokens: {response.usage.input_tokens}→{response.usage.output_tokens}]"
                )

            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                conversation.messages.pop()

        # 对话结束后，询问是否保存
        if conversation.get_message_count() > 0:
            save_choice = input("\n💾 是否保存对话？(y/n): ").strip().lower()
            if save_choice == "y":
                conversation.save_to_file()

        print("\n✅ 示例 2 完成")

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


# =====================================================
# 示例 3：流式输出对话
# =====================================================


def example_3_streaming_conversation():
    """
    示例 3：流式输出对话

    演示如何使用流式输出进行多轮对话
    实时显示 Claude 的回复，提升用户体验
    """
    print("\n" + "=" * 60)
    print("示例 3：流式输出对话")
    print("=" * 60)

    try:
        # 创建客户端和对话管理器
        client = config.create_client()
        if not client:
            return

        conversation = ConversationManager()

        print("\n开始流式输出对话演示...")

        # 第 1 轮对话
        print("\n" + "-" * 60)
        print("🗣️ 第 1 轮对话（流式输出）")
        print("-" * 60)

        user_msg_1 = "请用 3 个段落介绍一下 Python 的主要特点。"
        print(f"👤 用户: {user_msg_1}")
        conversation.add_user_message(user_msg_1)

        print("\n🤖 Claude (流式输出):")

        # 使用流式 API
        full_response = ""
        with client.messages.stream(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            messages=conversation.get_messages(),
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

        print()  # 换行
        conversation.add_assistant_message(full_response)

        # 第 2 轮对话
        print("\n" + "-" * 60)
        print("🗣️ 第 2 轮对话（流式输出）")
        print("-" * 60)

        user_msg_2 = "那 Python 最适合用来做什么？"
        print(f"👤 用户: {user_msg_2}")
        conversation.add_user_message(user_msg_2)

        print("\n🤖 Claude (流式输出):")

        full_response_2 = ""
        with client.messages.stream(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            messages=conversation.get_messages(),
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response_2 += text

        print()  # 换行
        conversation.add_assistant_message(full_response_2)

        # 显示对话统计
        print("\n" + "=" * 60)
        print("📊 对话统计")
        print("=" * 60)
        print(f"总消息数: {conversation.get_message_count()}")
        print(f"对话轮数: {conversation.get_message_count() // 2}")

        print("\n✅ 示例 3 完成")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")


# =====================================================
# 示例 4：带系统提示的对话
# =====================================================


def example_4_conversation_with_system_prompt():
    """
    示例 4：带系统提示的对话

    演示如何使用系统提示（system prompt）来定制 Claude 的行为
    """
    print("\n" + "=" * 60)
    print("示例 4：带系统提示的对话")
    print("=" * 60)

    try:
        # 创建客户端和对话管理器
        client = config.create_client()
        if not client:
            return

        conversation = ConversationManager()

        # 定义系统提示
        system_prompt = """你是一位经验丰富的 Python 编程导师。
你的教学风格是：
1. 用简单易懂的语言解释复杂概念
2. 总是提供实际的代码示例
3. 鼓励学生动手实践
4. 对初学者保持耐心和友好

请用这种风格回答学生的问题。"""

        print(f"\n📝 系统提示:\n{system_prompt}")
        print("\n开始对话...")

        # 第 1 轮对话
        print("\n" + "-" * 60)
        print("🗣️ 第 1 轮对话")
        print("-" * 60)

        user_msg_1 = "什么是列表推导式？"
        print(f"👤 用户: {user_msg_1}")
        conversation.add_user_message(user_msg_1)

        response_1 = client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            system=system_prompt,  # 添加系统提示
            messages=conversation.get_messages(),
        )

        assistant_msg_1 = response_1.content[0].text
        print(f"\n🤖 Claude: {assistant_msg_1}")
        conversation.add_assistant_message(assistant_msg_1)

        # 第 2 轮对话
        print("\n" + "-" * 60)
        print("🗣️ 第 2 轮对话")
        print("-" * 60)

        user_msg_2 = "能给我一个更复杂的例子吗？"
        print(f"👤 用户: {user_msg_2}")
        conversation.add_user_message(user_msg_2)

        response_2 = client.messages.create(
            model=config.DEFAULT_MODEL,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            system=system_prompt,  # 保持相同的系统提示
            messages=conversation.get_messages(),
        )

        assistant_msg_2 = response_2.content[0].text
        print(f"\n🤖 Claude: {assistant_msg_2}")
        conversation.add_assistant_message(assistant_msg_2)

        print("\n✅ 示例 4 完成")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")


# =====================================================
# 主函数
# =====================================================


def main():
    """主函数：运行所有示例"""
    print("\n" + "=" * 60)
    print("Claude SDK 多轮对话示例")
    print("=" * 60)

    # 验证配置
    is_valid, error_msg = config.validate_config()
    if not is_valid:
        print(f"\n❌ 错误：{error_msg}")
        print("\n请先设置 API Key：")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        return

    print("\n✅ API Key 已配置")

    # 显示菜单
    print("\n请选择要运行的示例：")
    print("  1. 基础多轮对话")
    print("  2. 交互式对话循环")
    print("  3. 流式输出对话")
    print("  4. 带系统提示的对话")
    print("  5. 运行所有示例（除了交互式）")
    print("  0. 退出")

    try:
        choice = input("\n请输入选项 (0-5): ").strip()

        if choice == "1":
            example_1_basic_multi_turn()
        elif choice == "2":
            example_2_interactive_conversation()
        elif choice == "3":
            example_3_streaming_conversation()
        elif choice == "4":
            example_4_conversation_with_system_prompt()
        elif choice == "5":
            example_1_basic_multi_turn()
            example_3_streaming_conversation()
            example_4_conversation_with_system_prompt()
            print("\n" + "=" * 60)
            print("✅ 所有示例运行完成！")
            print("=" * 60)
        elif choice == "0":
            print("\n👋 再见！")
        else:
            print("\n⚠️ 无效选项")

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


if __name__ == "__main__":
    main()
