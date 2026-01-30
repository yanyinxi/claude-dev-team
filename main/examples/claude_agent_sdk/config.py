#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================
Claude SDK 配置文件
=====================================================
功能：统一管理 Claude SDK 的配置信息
作者：Claude Dev Team
创建时间：2026-01-25

本配置文件提供：
1. API Key 和 Base URL 的统一获取
2. Anthropic 客户端的统一创建
3. 配置验证和错误处理
=====================================================
"""

import os
from typing import Optional

from anthropic import Anthropic

# =====================================================
# 配置常量
# =====================================================

# 可用的模型列表（按推荐顺序）
AVAILABLE_MODELS = {
    "haiku": "claude-haiku-4-5-20251001",       # 推荐：速度最快，便宜￥5 / M tokens
    "sonnet": "claude-sonnet-4-5-20250929"    # 推荐：性能最好 中等￥18 / M tokens
 
}

# 默认模型（优先使用环境变量，否则使用 haiku）
DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", AVAILABLE_MODELS["haiku"])

# 默认 max_tokens
DEFAULT_MAX_TOKENS = 1024


# =====================================================
# 配置获取函数
# =====================================================

def get_api_key() -> Optional[str]:
    """
    获取 API Key

    Returns:
        str: API Key，如果未设置则返回 None
    """
    return os.getenv("ANTHROPIC_API_KEY")


def get_base_url() -> Optional[str]:
    """
    获取 Base URL

    Returns:
        str: Base URL，如果未设置则返回 None
    """
    return os.getenv("ANTHROPIC_BASE_URL")


def validate_config() -> tuple[bool, str]:
    """
    验证配置是否完整

    Returns:
        tuple[bool, str]: (是否有效, 错误信息)
    """
    api_key = get_api_key()

    # API Key 是必需的
    if not api_key:
        return False, "未设置 ANTHROPIC_API_KEY 环境变量"

    # Base URL 是可选的（只在使用自定义端点时需要）
    base_url = get_base_url()
    if base_url:
        print(f"ℹ️  使用自定义 Base URL: {base_url}")

    return True, ""


# =====================================================
# 客户端创建函数
# =====================================================

def create_client() -> Optional[Anthropic]:
    """
    创建 Anthropic 客户端

    Returns:
        Anthropic: 客户端实例，如果配置无效则返回 None
    """
    # 验证配置
    is_valid, error_msg = validate_config()
    if not is_valid:
        print(f"❌ 错误：{error_msg}")
        return None

    # 获取配置
    api_key = get_api_key()
    base_url = get_base_url()

    # 创建客户端（只在 base_url 存在时传递）
    # 设置超时时间为 10 分钟（600 秒），避免长请求超时
    if base_url:
        print(f"ℹ️  使用自定义 Base URL: {base_url}")
        return Anthropic(base_url=base_url, api_key=api_key, timeout=600.0)
    else:
        return Anthropic(api_key=api_key, timeout=600.0)
    

# =====================================================
# 配置信息显示
# =====================================================

def print_config_info():
    """打印配置信息（用于调试）"""
    print("\n" + "="*60)
    print("Claude SDK 配置信息")
    print("="*60)

    api_key = get_api_key()
    base_url = get_base_url()

    if api_key:
        # 只显示前 8 位和后 4 位
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print(f"✅ API Key: {masked_key}")
    else:
        print("❌ API Key: 未设置")

    if base_url:
        print(f"✅ Base URL: {base_url}")
    else:
        print("ℹ️  Base URL: 使用默认值")

    print(f"ℹ️  默认模型: {DEFAULT_MODEL}")
    print(f"ℹ️  默认 max_tokens: {DEFAULT_MAX_TOKENS}")
    print("="*60)
