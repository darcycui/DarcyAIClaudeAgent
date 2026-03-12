from openai import OpenAI

from utils.api_key_util import get_api_key_deepseek


def init_client():
    """Initialize the OpenAI client."""
    api_key = get_api_key_deepseek()
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )



if __name__ == '__main__':
    print(f"使用 API key: {get_api_key_deepseek()} 访问 DeepSeek 模型 api")
    client = init_client()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is DeepSeek?"},
        ],
        max_tokens=1024,
        temperature=0.7,
        stream=False, # 这里不使用流式（逐步返回生成的文本）
    )
    print(response.choices[0].message.content)
