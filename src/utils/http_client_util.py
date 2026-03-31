import json
from traceback import print_stack

import httpx


def log_request(request):
    print("============ Outgoing Request ============")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    # 记录请求体
    if hasattr(request, 'content'):
        try:
            if isinstance(request.content, (bytes, bytearray)):
                body = request.content.decode('utf-8')
            else:
                body = str(request.content)
            try:
                body_json = json.loads(body)
                print("Body (JSON):")
                print(json.dumps(body_json, indent=2, ensure_ascii=False))
            except json.JSONDecodeError as e:
                print(f"出现异常：{e}")
                # 打印堆栈
                print_stack()
                print(f"Body: {body}")
        except Exception as e:
            print(f"Body: [Unable to read: {e}]")
    print("===============================")


def log_response(response):
    print("=========== Incoming Response ===========")
    print(f"Status: {response.status_code}")
    # 读取响应内容
    try:
        response.read()  # 这步很重要！
        content = response.text

        # 尝试美化JSON输出
        try:
            content_json = json.loads(content)
            print("Content (JSON):")
            print(json.dumps(content_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"出现异常：{e}")
            # 限制输出长度
            if len(content) > 1000:
                print(f"Content: {content[:1000]}...")
            else:
                print(f"Content: {content}")

    except Exception as e:
        print(f"Error reading response content: {e}")
    print("==============================")


# 创建自定义 HTTP client
http_client = httpx.Client(
    verify=False,
    event_hooks={
        'request': [log_request],
        'response': [log_response],
    }
)
