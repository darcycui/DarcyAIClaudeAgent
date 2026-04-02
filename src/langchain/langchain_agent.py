import asyncio

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage

from src.langchain.langchain_api_call import llm_client
from src.langchain.mcps.mcp_adapter import get_mcp_tools
from src.langchain.middleware.agent_aop import before_agent_aop
from src.langchain.middleware.model_aop import before_model_aop, after_model_aop
from src.langchain.middleware.skill_middleware import SkillMiddleware
from src.langchain.prompt.system_prompt import system_prompt
from src.langchain.tools.test_tool import math_add


async def main():
    # 获取 MCP 工具
    mcp_tools = await get_mcp_tools()

    # 创建 Agent
    agent = create_agent(
        model=llm_client,  # 模型
        system_prompt=system_prompt,  # 系统提示
        tools=[math_add] + mcp_tools,  # 工具、MCP
        middleware=[SkillMiddleware()],  # 中间拦截器
        # middleware=[SkillMiddleware(), before_agent_aop, before_model_aop, after_model_aop],  # 中间拦截器
    )
    # 调用 Skill
    agent_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="翻转文本 ' hello  world '"),
        # AIMessage(content=""),
    ]
    # # 调用 Skill
    # agent_messages = [
    #     SystemMessage(content=system_prompt),
    #     HumanMessage(content="格式化文本 ' hello  world '"),
    #     # AIMessage(content=""),
    # ]
    # # 调用 MCP
    # agent_messages = [
    #     SystemMessage(content=system_prompt),
    #     HumanMessage(content="北京的天气"),
    #     # AIMessage(content=""),
    # ]

    # # 调用 tool
    # agent_messages = [
    #     {"role": "user", "content": "计算1+2"},
    #     {"role": "assistant", "content": ""},
    # ]

    # # chat
    # agent_messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": "你好"},
    #     {"role": "assistant", "content": ""},
    # ]
    messages_dict = {"messages": agent_messages}
    response = await agent.ainvoke(messages_dict, print_mode="values")
    print("==============================")
    for m in response["messages"]:
        type_name = m.__class__.__name__
        print(f"{type_name} {m.content}")


if __name__ == "__main__":
    """同步入口，运行异步主函数"""
    asyncio.run(main())
