from openai import OpenAI

from utils.api_key_util import get_api_key_deepseek


def init_client():
    """Initialize the OpenAI client."""
    api_key = get_api_key_deepseek()
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

def main():
    print(f"使用 API key: {get_api_key_deepseek()} 访问 DeepSeek 模型 api")
    client = init_client()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位专业聊天助手."},
            {"role": "user", "content": "什么是DeepSeek?"},
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

if __name__ == '__main__':
    main()
