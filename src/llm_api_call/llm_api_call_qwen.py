import traceback

import dashscope  # 调用Qwen大模型
from http import HTTPStatus  # 检查与Qwen模型HTTP请求状态

from dashscope.api_entities.dashscope_response import Message

from src.utils.api_key_util import get_api_key_qwen

"""
Qwen llm api
"""
# 设置Qwen系列具体模型及对应的调用API密钥，从阿里云百炼大模型服务平台获得
model_name = "qwen-turbo"
model_api_key = get_api_key_qwen()


def call_llm_api(query, chunks):
    """
    生成流程：调用 Qwen 大模型 api，根据查询和文本块生成最终回复
    :param query: 用户查询语句
    :param chunks: 检索到的相关文本块
    :return: 最终回复
    """
    # 设置Qwen系列具体模型及对应的调用API密钥，从阿里云大模型服务平台百炼获得
    llm_model = model_name
    dashscope.api_key = model_api_key

    # 构建参考文档内容 格式为：[参考文档1] \n [参考文档2] \n ...
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[参考文档{i + 1}] \n {chunk} \n\n"

    # 构建生成模型所需的Prompt，包含用户查询和检索到的相关文本块
    prompt = f"根据参考文档回答问题：{query}\n\n{context}"
    print(f"生成模型的Prompt: {prompt}")

    # 准备请求消息，将prompt作为输入
    messages = [Message(role="user", content=prompt)]

    # 调用大模型API云服务生成响应
    try:
        responses = dashscope.Generation.call(
            model=llm_model,
            messages=messages,
            result_format='message',  # 设置返回格式为"message"
            stream=True,  # 启用流式输出
            incremental_output=True  # 获取流式增量输出
        )
        # 初始化变量以存储生成的响应内容
        generated_response = ""
        print("生成过程开始:")
        # 逐步获取和处理模型的增量输出
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0]['message']['content']
                generated_response += content
                print(content, end='')  # 实时输出模型生成的内容
            else:
                print(f"请求失败: {response.status_code} - {response.message}")
                return None  # 请求失败时返回 None
        print("\n生成过程完成.")
        return generated_response
    except Exception as e:
        print(f"调用大模型API云服务异常: {e}")
        # 打印堆栈
        traceback.print_exc()
        return "抱歉，回答出错。"


if __name__ == '__main__':
    query_word = "下面报告中涉及了哪几个行业的案例以及总结各自面临的挑战？"
    call_llm_api(query_word, [])
