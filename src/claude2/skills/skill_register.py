import subprocess
import sys
from pathlib import Path
from typing import Any, Callable
from venv import logger

from langchain.tools import tool

from src.claude2.skills.skill import Skill
from src.claude2.skills.skill_parser import load_skills_dynamically

# 动态解析 Skills
SKILLS: list[Skill] = load_skills_dynamically()


def load_skill_with_script(skill_name, skill):
    """加载包含 scripts 的技能信息"""
    script_paths = skill.get("script_paths", [])
    if not script_paths:
        return f"加载 Skill: {skill_name}\n\n{skill['content']}"

    # 只返回技能内容和脚本路径信息，不解析函数
    scripts_info = "\n\n## 可用脚本：\n"
    for script_path in script_paths:
        script_file = Path(script_path).name
        scripts_info += f"- **{script_file}**: 可执行此脚本处理任务\n"
    return f"加载 Skill: {skill_name}\n\n{skill['content']}{scripts_info}"

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
            # 检查是否包含 scripts
            if skill.get("script_paths") and len(skill.get("script_paths", [])) > 0:
                return load_skill_with_script(skill_name, skill)
            return f"加载 Skill: {skill_name}\n\n{skill['content']}"
    # 未找到Skill
    available = ", ".join(s["name"] for s in SKILLS)
    return f"未找到Skill: '{skill_name}' . 可用Skills: {available}"


# 通用的动态技能工具
@tool
def execute_skill_script(skill_name: str, script_filename: str, parameters: dict[str, Any] = None) -> str:
    """
    执行指定技能的脚本文件（通过命令行方式）
    Args:
        skill_name: 技能名称
        script_filename: 脚本文件名（例如：format_text.py）
        parameters: 传递给脚本的参数（字典形式，会被转换为命令行参数）
    Returns:
        脚本执行结果或错误信息
    """
    from pathlib import Path

    # 查找技能
    skill = None
    for s in SKILLS:
        if s["name"] == skill_name:
            skill = s
            break

    if not skill:
        return f"未找到技能：{skill_name}"

    # 检查脚本路径列表
    script_paths = skill.get("script_paths", [])
    if not script_paths:
        return f"技能 '{skill_name}' 没有关联的脚本文件"

    # 查找匹配的脚本文件
    script_path = None
    for path in script_paths:
        if Path(path).name == script_filename:
            script_path = path
            break

    # 验证文件名是否匹配
    if not script_path:
        available_scripts = [Path(p).name for p in script_paths]
        return f"技能 '{skill_name}' 中没有找到脚本文件 '{script_filename}'。可用脚本：{', '.join(available_scripts)}"

    # 构建命令行参数
    cmd_args = [sys.executable, script_path]

    # 将参数字典转换为命令行参数
    if parameters:
        # 如果 parameters 是字典，提取值作为参数
        if isinstance(parameters, dict):
            # 优先使用 'text' 或 'input' 键的值
            param_value = parameters.get('text') or parameters.get('input') or parameters.get('data')
            if param_value:
                cmd_args.append(str(param_value))
            else:
                # 如果没有标准键，尝试使用第一个值
                first_value = next(iter(parameters.values()), None)
                if first_value:
                    cmd_args.append(str(first_value))
        else:
            # 如果 parameters 不是字典，直接添加
            cmd_args.append(str(parameters))

    logger.info(f"=== 开始执行脚本 ===")
    logger.info(f"技能名称：{skill_name} 脚本文件：{script_filename} 命令：{' '.join(cmd_args)}")

    try:
        # 执行脚本并捕获输出
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30  # 30 秒超时
        )

        # 返回标准输出和标准错误
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            logger.error(f"脚本执行失败：{error}")
            return f"执行脚本失败：{script_filename}\n错误信息：{error}"

        # 将输出按行分割，只返回最后一行作为结果（前面的行是日志）
        output_lines = output.split('\n')
        result_line = output_lines[-1].strip() if output_lines else ""
        logger.info(f"成功执行脚本：{script_filename} 输出：{output}")
        return result_line if result_line else "脚本执行成功（无输出）"

    except subprocess.TimeoutExpired:
        logger.error(f"脚本执行超时：{script_filename}")
        return f"执行脚本超时：{script_filename}（超过 30 秒）"
    except Exception as e:
        logger.error(f"执行脚本时出错 {script_filename}: {e}")
        return f"执行脚本失败：{script_filename}\n错误：{str(e)}"

# 更新工具列表
def get_all_skill_tools():
    """获取所有 Skill 工具"""
    return [load_skill, execute_skill_script]
