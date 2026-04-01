from typing import Any, Callable
from venv import logger

from langchain.tools import tool

from src.langchain.skills.skill import Skill, load_skill_functions

SKILLS: list[Skill] = [
    {
        "name": "go_out_tips",
        "description": "用于提醒出门携带物品清单",
        "content": """
        
        ## 示例
        必带物品：
        手机
        钱包
        钥匙
        
        选带物品：
        雨伞
        
        """,
        "script_path": "",  # 无脚本
        "functions": {}
    },
    {  # 新增的 my-first-skill
        "name": "my-first-skill",
        "description": "通过删除多余空格、修正大小写和纠正标点符号来格式化和清理文本内容",
        "content": """
        # 文本格式化器
        当被要求格式化文本时：
        1.  使用  脚本scripts/process.py 中的`format_text`工具来处理文本。
        2.  该工具会执行以下操作：
            - 删除多余空格（将多个空格替换为单个空格）
            - 修正大小写（句子首字母大写）
            - 纠正标点符号（确保以句号、感叹号或问号结束）
        3.  将工具返回的结果提供给用户。

        ## 示例
        **用户输入**: "hello   world"
        **预期结果**: "Hello world."

        **用户输入**: "this is  a    test"
        **预期结果**: "This is a test."

        ## 指南
        - 保留有意的格式（如换行、段落）。
        - 不要更改技术术语或专有名词。
        - 保持原始语言和语气。
        """,
        "script_path": "D:/Projectss/AI/DarcyClaudeAgent/config/skills/my-first-skill/scripts/process.py",  # 指定脚本路径
        "functions": {}  # 初始为空，在需要时动态加载
    }
]


def load_skill_with_script(skill_name, skill):
    try:
        functions = load_skill_functions(skill_name, skill["script_path"])
        skill["functions"] = functions

        # 将函数信息添加到技能内容中
        if functions:
            functions_info = "\n\n## 可用函数：\n"
            for func_name, func_info in functions.items():
                functions_info += f"- **{func_name}{func_info['signature']}**: {func_info['docstring']}\n"
            return f"加载 Skill: {skill_name}\n\n{skill['content']}{functions_info}"
    except Exception as e:
        logger.error(f"加载技能函数时出错 {skill_name}: {e}")
        # 未找到Skill
        available = ", ".join(s["name"] for s in SKILLS)
        return f"未找到Skill: '{skill_name}' . 可用Skills: {available}"


@tool
def load_skill(skill_name: str) -> str:
    """将技能的全部内容加载到代理的上下文中。
    当你需要关于如何处理特定类型请求的详细信息时，可以使用它。这将为您提供技能领域的全面说明、政策和指导方针。
    Args:
        skill_name: skill的名称
    """
    # 遍历Skills
    for skill in SKILLS:
        if skill["name"] == skill_name:
            # 检查是否需要加载脚本函数
            if skill.get("script_path") and not skill.get("functions"):
                return load_skill_with_script(skill_name, skill)
            return f"加载 Skill: {skill_name}\n\n{skill['content']}"
    # 未找到Skill
    available = ", ".join(s["name"] for s in SKILLS)
    return f"未找到Skill: '{skill_name}' . 可用Skills: {available}"


# 通用的动态技能工具
@tool
def execute_skill_function(skill_name: str, function_name: str,  parameters: dict[str, Any] = None) -> str:
    """
    动态执行指定技能的函数
    Args:
        skill_name: 技能名称
        function_name: 要执行的函数名称
        parameters: 传递给函数的参数
    Returns:
        函数执行结果或错误信息
    """
    # 查找技能
    skill = None
    for s in SKILLS:
        if s["name"] == skill_name:
            skill = s
            break
    if not skill:
        return f"未找到技能: {skill_name}"
    # 确保脚本路径存在
    script_path = skill.get("script_path")
    if not script_path:
        return f"技能 '{skill_name}' 没有关联的脚本文件"
    # 动态加载函数（如果尚未加载）
    if not skill.get("functions"):
        functions = load_skill_functions(skill_name, script_path)
        skill["functions"] = functions
        if not functions:
            return f"技能 '{skill_name}' 的脚本中没有找到可用的函数"
    functions = skill["functions"]
    # 检查函数是否存在
    if function_name not in functions:
        available_funcs = ", ".join(functions.keys())
        return f"函数 '{function_name}' 在技能 '{skill_name}' 中不存在。可用函数: {available_funcs}"
    func_info = functions[function_name]
    func: Callable[..., Any] = func_info['function']
    logger.info(f"=== 开始执行函数 ===")
    logger.info(f"技能名称：{skill_name} 函数名称：{function_name} 参数字典：{parameters}")
    if parameters:
        logger.info("parameters 详细内容:")
        for key, value in parameters.items():
            logger.info(f"  - {key}: {value} (类型：{type(value).__name__})")
    try:
        # 动态调用函数
        result: Any = func(**parameters)
        # 记录调用信息
        logger.info(f"成功执行函数: {skill_name}.{function_name} 参数: {parameters}")
        return str(result)
    except Exception as e:
        logger.error(f"执行函数时出错 {skill_name}.{function_name}: {e}")

        # 返回有用的错误信息，包括函数签名
        return f"执行函数失败: {function_name}{func_info['signature']}\n错误: {str(e)}\n需要参数: {', '.join(func_info['parameters'])}"


# 获取技能可用函数的工具
@tool
def list_skill_functions(skill_name: str) -> str:
    """
    列出指定技能中所有可用的函数
    Args:
        skill_name: 技能名称
    Returns:
        函数列表信息
    """
    skill = None
    for s in SKILLS:
        if s["name"] == skill_name:
            skill = s
            break
    if not skill:
        return f"未找到技能: {skill_name}"
    script_path = skill.get("script_path")
    if not script_path:
        return f"技能 '{skill_name}' 没有关联的脚本文件"
    # 动态加载函数
    if not skill.get("functions"):
        functions = load_skill_functions(skill_name, script_path)
        skill["functions"] = functions
    else:
        functions = skill["functions"]
    if not functions:
        return f"技能 '{skill_name}' 的脚本中没有找到可用的函数"
    result = f"技能 '{skill_name}' 中的可用函数 ({len(functions)} 个):\n\n"
    for func_name, func_info in functions.items():
        result += f"**{func_name}**\n"
        result += f"- 签名: {func_info['signature']}\n"
        result += f"- 参数: {', '.join(func_info['parameters'])}\n"
        result += f"- 说明: {func_info['docstring']}\n\n"
    return result


# 更新工具列表
def get_all_skill_tools():
    """获取所有 Skill 工具"""
    return [load_skill, execute_skill_function, list_skill_functions]
