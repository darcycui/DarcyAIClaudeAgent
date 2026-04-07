from typing import TypedDict


class Skill(TypedDict):
    """技能类 保存技能相关信息"""
    name: str
    description: str
    content: str
    script_paths:  list[str]  # 修改为支持多个脚本路径