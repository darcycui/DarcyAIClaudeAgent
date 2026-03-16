import os
import sys


def get_api_key_deepseek() -> str:
    """获取DeepSeek的API Key"""
    return get_api_key_by_name("DEEPSEEK_API_KEY")


def get_api_key_zhipu_glm() -> str:
    """获取智谱的API Key"""
    return get_api_key_by_name("ZHIPU_API_KEY")


def get_api_key_by_name(env_name: str) -> str:
    """获取DeepSeek的API Key"""
    api_key = os.environ.get(env_name)
    if not api_key:
        print("Error: please set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)
    return api_key
