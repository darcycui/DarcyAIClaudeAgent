from typing import TypedDict, List, Any, Optional, Callable
import re
from pathlib import Path
from src.claude2.skills.skill import Skill


def parse_skill_md(skill_dir: Path) -> dict[str, str | list[Any] | dict[Any, Any]] | None:
    """
    解析 SKILL.md 文件
    Args:
        skill_dir: 技能目录路径
    Returns:
        解析后的 Skill 字典，如果解析失败则返回 None
    """
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return None
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 解析 YAML front matter
        if not content.startswith("---"):
            return None
        # 找到第二个 ---
        end_marker = content.find("---", 3)
        if end_marker == -1:
            return None
        # 提取 front matter 和内容
        front_matter = content[4:end_marker].strip()
        skill_content = content[end_marker + 3:].strip()
        # 解析 front matter 中的 name 和 description
        name_match = re.search(r'name:\s*(.+)', front_matter)
        desc_match = re.search(r'description:\s*(.+)', front_matter)
        if not name_match or not desc_match:
            return None
        name = name_match.group(1).strip()
        description = desc_match.group(1).strip()
        # 检查是否有 scripts 子目录
        scripts_dir = skill_dir / "scripts"
        script_paths = []
        if scripts_dir.exists() and any(scripts_dir.iterdir()):
            # 获取 scripts 目录下所有的 .py 文件
            for py_file in scripts_dir.glob("*.py"):
                if not py_file.name.startswith('_'):  # 跳过私有文件
                    script_paths.append(str(py_file.absolute()))
        return {
            "name": name,
            "description": description,
            "content": skill_content,
            "script_paths": script_paths,
            "functions": {}
        }
    except Exception as e:
        print(f"解析 SKILL.md 失败 {skill_md_path}: {e}")
        return None


def load_skills_dynamically() -> List[Skill]:
    """
    动态加载 config/skills 目录中的所有技能
    Returns:
        所有技能的列表
    """
    skills = []
    # 获取 skills 目录
    skills_dir = Path(__file__).parent.parent.parent.parent / "config" / "skills"
    if not skills_dir.exists():
        print(f"Skills 目录不存在：{skills_dir}")
        return skills
    # 遍历所有子目录
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill = parse_skill_md(skill_dir)
            if skill:
                skills.append(skill)
                print(f"已加载技能：{skill['name']}")
    return skills

