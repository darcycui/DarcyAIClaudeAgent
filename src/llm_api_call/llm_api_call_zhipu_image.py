from zai import ZhipuAiClient

from src.utils.api_key_util import get_api_key_zhipu_glm

"""
zhipu GLM llm-image api
"""


def main():
    print(f"使用 API key: {get_api_key_zhipu_glm()} 访问 ZhipuAi 模型 api")
    client = ZhipuAiClient(api_key=get_api_key_zhipu_glm())  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4.6v-flash",  # 填写需要调用的模型名称
        messages=[
            {
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            # 远程图片 url
                            "url": "https://cdn.bigmodel.cn/static/logo/register.png"
                        }
                    },
                    {
                        "type": "text",
                        "text": "描述这张照片。并找到二维码的位置 以[[xmin,ymin,xmax,ymax]]格式回答"
                    }
                ],
                "role": "user"
            }
        ],
        thinking={
            "type": "enabled"
        },
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.reasoning_content:
            print(chunk.choices[0].delta.reasoning_content, end='', flush=True)

        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)


if __name__ == '__main__':
    main()
