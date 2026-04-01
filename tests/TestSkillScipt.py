import logging
import unittest

from src.langchain.skills.skill_register import list_skill_functions, execute_skill_function


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

    def test_list_skill_functions_tool(self):
        result = list_skill_functions.invoke({"skill_name": "my-first-skill"})
        print(f"result={result}")

    def test_execute_skill_function(self):
        result = execute_skill_function("my-first-skill", "format_text", text="  hello  world  ")
        print(f"result={result}")

    def test_execute_skill_function_tool(self):
        result_expected = "Hello world."
        result = execute_skill_function.invoke({
            "skill_name": "my-first-skill",
            "function_name": "format_text",
            "parameters": {"text": "  hello  world  "}
        })
        print(f"result={result}")
        self.assertEqual(result_expected, result, "函数调用失败")


if __name__ == '__main__':
    unittest.main()
