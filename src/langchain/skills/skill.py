import importlib.util
import inspect
import sys
from pathlib import Path
from typing import TypedDict, Callable, Any
from venv import logger


class Skill(TypedDict):
    """A skill that can be progressively disclosed to the agent."""
    name: str
    description: str
    content: str
    script_path: str  # 新增：存储脚本路径
    functions: dict[str, Any]  # 新增：存储解析到的函数


# 动态加载和缓存技能的脚本函数
_skill_functions_cache: dict[str, dict[str, Callable]] = {}


def load_skill_functions(skill_name: str, script_path: str) -> dict[str, Callable]:
    """
    动态加载技能脚本中的所有函数

    Args:
        skill_name: 技能名称
        script_path: 脚本文件相对路径

    Returns:
        字典，键为函数名，值为函数对象
    """
    if skill_name in _skill_functions_cache:
        logger.info(f"从缓存中获取技能函数: {skill_name}")
        return _skill_functions_cache[skill_name]

    functions = {}

    try:
        # 确保脚本路径存在

        script_path_obj = Path(script_path)
        if not script_path_obj.exists():
            logger.warning(f"技能脚本不存在: {script_path}")
            return functions

        # 动态导入模块
        # 为模块创建一个唯一的名称
        module_name = f"skill_{skill_name.replace('-', '_')}_module"

        # 使用 importlib 动态导入
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec is None or spec.loader is None:
            logger.error(f"无法创建模块规范: {script_path}")
            return functions

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(f"执行模块时出错 {module_name}: {e}")
            return functions

        # 获取模块中的所有函数
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                # 获取函数的参数信息
                sig = inspect.signature(obj)
                params = list(sig.parameters.keys())
                functions[name] = {
                    'function': obj,
                    'signature': str(sig),
                    'parameters': params,
                    'docstring': inspect.getdoc(obj) or f"{name} 函数"
                }

                logger.info(f"从技能: {skill_name} 加载函数: {name}{sig} ")

        # 缓存结果
        _skill_functions_cache[skill_name] = functions
        logger.info(f"成功加载 {len(functions)} 个函数从技能: {skill_name}")

    except Exception as e:
        logger.error(f"动态加载技能函数时出错 {skill_name}: {e}")

    return functions
