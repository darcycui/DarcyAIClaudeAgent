import requests
from openai import OpenAI


def call_llama(prompt):
    """
    调用本地 llama.cpp API
    """
    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "model": "",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )
    print(response.json()["choices"][0]["message"]["content"])

def call_llama_stream(prompt):
    """
    流式调用本地 llama.cpp API
    :param prompt: 提示词
    """
    client = OpenAI(
        api_key="",
        base_url="http://localhost:8000/v1",
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位专业聊天助手."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
        temperature=0.7,
        # stream=False,  # 不使用流式
        stream=True,  # 使用流式（逐步返回生成的文本）
    )
    # 不使用流式处理，获取完整回复
    # print(response.choices[0].message.content)
    # 流式处理响应
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()  # 换行

if __name__ == "__main__":
    # call_llama("请介绍一下你自己")
    call_llama_stream("请介绍一下你自己")