import os
import sys


def get_api_key_deepseek() -> str:
    """获取DeepSeek的API Key"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: please set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)
    return api_key
