from typing import Any

from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from typing import Callable

from src.langchain.skills.skill_register import SKILLS, get_all_skill_tools

"""
拦截器：添加 Skills
"""


class SkillMiddleware(AgentMiddleware):
    """拦截器 用于将 Skills 的 name、description 添加到 系统提示词"""

    # 注册 Skill 相关工具
    tools = get_all_skill_tools()

    def __init__(self):
        """
        初始化 skills_prompt
        """
        skills_list = []
        for skill in SKILLS:
            description = skill["description"]
            # 如果技能有脚本，在描述中添加提示
            if skill.get("script_path"):
                description += f" [此技能有可执行脚本: {skill.get('script_path')}]"
            skills_list.append(f"- **{skill['name']}**: {description}")
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """同步拦截 将 Skill 添加到系统提示词"""
        modified_request = self._build_modified_request(request)
        return handler(modified_request)

    async def awrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], Any],
    ) -> Any:
        """异步拦截 将 Skill 添加到系统提示词"""
        modified_request = self._build_modified_request(request)
        return await handler(modified_request)

    def _build_modified_request(self, request: ModelRequest) -> ModelRequest:
        # 复制请求
        modified_messages = [msg for msg in request.messages]

        # 找到第一条系统消息 SystemMessage
        # 在系统消息中添加 skills_prompt
        system_message_index = 0
        for i, msg in enumerate(modified_messages):
            if isinstance(msg, SystemMessage):
                system_message_index = i
                break

        original_content = ""
        if system_message_index is not None:
            original_content = modified_messages[system_message_index].content
        else:
            print("未找到系统消息")

        modified_messages[system_message_index] = SystemMessage(
            content=f"{original_content}\n\n## 可用技能列表\n{self.skills_prompt}\n\n## 工具使用说明\n"
                    f"1. 使用 `load_skill` 工具获取技能的详细指令\n"
                    f"2. 使用 `execute_skill_function` 工具执行技能脚本中的函数\n"
                    f"3. 使用 `list_skill_functions` 工具查看技能的所有可用函数"
        )
        return request.override(messages=modified_messages)
