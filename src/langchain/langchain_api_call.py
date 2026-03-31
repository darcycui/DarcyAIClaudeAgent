from dashscope import api_key
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from src.langchain.prompt.system_prompt import system_prompt
from src.utils.api_key_util import get_api_key_deepseek
from src.utils.http_client_util import http_client

llm_client = init_chat_model(
    model="deepseek-chat",
    api_key=get_api_key_deepseek(),
    # http_client=http_client,
)


def main():
    # 方法 1: 简单的两轮对话（推荐）
    # 使用 SystemMessage 和 HumanMessage 和 AIMessage
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="你好"),
        # AIMessage(content=""),
    ]
    # # 或 使用 system user assistant
    # messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": "你好"},
    #     {"role": "assistant", "content": ""},
    # ]
    response: AIMessage = llm_client.invoke(messages)
    print(response.content)

    # 方法 2: 多轮对话 - 保存历史消息
    # messages = [
    #     SystemMessage(content="你是一位资深程序员"),
    #     HumanMessage(content="你好"),
    #     response,  # AI 的上一次回复
    #     HumanMessage(content="请介绍一下你自己"),
    # ]
    # response: AIMessage = client.invoke(messages)
    # print(response.content)


if __name__ == '__main__':
    main()
