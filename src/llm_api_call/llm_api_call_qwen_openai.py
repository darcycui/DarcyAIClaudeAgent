import traceback
from dashscope.api_entities.dashscope_response import Message
from openai import OpenAI
from src.utils.api_key_util import get_api_key_qwen

"""
Qwen llm api
"""
# 设置Qwen系列具体模型及对应的调用API密钥，从阿里云百炼大模型服务平台获得
model_name = "qwen-plus"
model_api_key = get_api_key_qwen()


def call_llm_api(query):
    """
    生成流程：调用 Qwen 大模型 api，根据查询和文本块生成最终回复
    :param query: 用户查询语句
    :return: 最终回复
    """

    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
        api_key=model_api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 构建提示词
    prompt = f"{query}"
    print(f"Prompt: {prompt}")

    # 准备请求消息，将prompt作为输入
    messages = [Message(role="user", content=prompt)]

    # 调用大模型API云服务生成响应
    try:
        # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
        responses = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': '你是以为AI助手.'},
                {'role': 'user', 'content': prompt}
            ],
            stream=True,
            stream_options={"include_usage": True}
        ) # ignore

        print("生成过程开始:")
        for chunk in responses:
            if chunk.choices[0].finish_reason:
                print(f"\nfinish_reason: {chunk.choices[0].finish_reason}")
                print(f"usage: {chunk.usage}")
                break
            print(chunk.choices[0].delta.content, end='')

        print("\n生成过程完成.")
    except Exception as e:
        print(f"调用大模型API云服务异常: {e}")
        # 打印堆栈
        traceback.print_exc()
        return "抱歉，回答出错。"


if __name__ == '__main__':
    query_word = "你好"
    call_llm_api(query_word)
