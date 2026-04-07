import logging
import unittest

from src.claude2.skills.skill import Skill
from src.claude2.skills.skill_parser import load_skills_dynamically


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """在模块加载前配置日志。"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()  # logger日志 输出到控制台
            ]
        )

    def test_parse_skill_md(self):
        skills: list[Skill] = load_skills_dynamically()
        print(skills)
        skills_list = []
        for skill in skills:
            description = skill["description"]
            # 如果技能有脚本，在描述中添加提示
            if skill.get("script_paths"):
                description += f" [此技能有可执行脚本: {skill.get('script_paths')}]"
            skills_list.append(f"- **{skill['name']}**: {description}")
        skills_prompt = "\n".join(skills_list)
        print(skills_prompt)


if __name__ == '__main__':
    unittest.main()
