from langchain_core.tools import tool


@tool
def math_add(a: int, b: int) -> int:
    """计算两个数字的和"""
    return a + b
