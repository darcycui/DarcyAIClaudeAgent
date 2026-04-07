import logging
import unittest

from src.claude2.skills.skill_register import execute_skill_script


def setUpModule():
    """在模块加载前配置日志。"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # logger日志 输出到控制台
        ]
    )


class TestSkillScript(unittest.TestCase):

    def test_execute_format_text_skill_tool(self):
        result_expected = "Hello world."
        result = execute_skill_script.invoke({
            "skill_name": "format-text-skill",
            "script_filename": "format_text.py",
            "parameters": {"text": "  hello  world  "}
        })
        print(f"result={result}")
        self.assertEqual(result_expected, result, "脚本调用失败")


    def test_execute_reverse_text_skill_tool(self):
        result_expected = "dlrow  olleh"
        result = execute_skill_script.invoke({
            "skill_name": "reverse-text-skill",
            "script_filename": "reverse_text.py",
            "parameters": {"text": "hello  world"}
        })
        print(f"result={result}")
        self.assertEqual(result_expected, result, "脚本调用失败")


if __name__ == '__main__':
    unittest.main()
