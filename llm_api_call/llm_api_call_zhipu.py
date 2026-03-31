from zai import ZhipuAiClient

from utils.api_key_util import get_api_key_zhipu_glm


def main():
    print(f"使用 API key: {get_api_key_zhipu_glm()} 访问 ZhipuAi 模型 api")
    client = ZhipuAiClient(api_key=get_api_key_zhipu_glm())  # 请填写您自己的 API Key

    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
            {"role": "assistant", "content": ""},
            {"role": "system", "content": "你是一位资深程序员，精通多种编程语言."},
            {"role": "user", "content": "什么是智谱GLM?"},
        ],
        thinking={
            "type": "false",  # 不启用深度思考模式
        },
        max_tokens=65536,  # 最大输出 tokens
        temperature=1.0,  # 控制输出的随机性
        # stream=False,  # 不使用流式
        stream=True,  # 使用流式（逐步返回生成的文本）
    )

    # 不使用流式 获取完整回复
    # print(response.choices[0].message)

    # 流式获取回复
    for chunk in response:
        if chunk.choices[0].delta.reasoning_content:
            print(chunk.choices[0].delta.reasoning_content, end='', flush=True)

        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)


if __name__ == '__main__':
    main()
