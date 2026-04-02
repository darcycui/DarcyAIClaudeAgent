# scripts/process.py
import sys


def reverse_text(text):
    """翻转文本"""
    print('原始文本：', text)
    text = text[::-1]
    print('翻转后的文本：', text)
    return text

if __name__ == '__main__':
    # 解析命令行参数 得到输入文本 text
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
    else:
        raise ValueError('请提供要处理的文本')
    formatted_text = reverse_text(input_text)
    print(formatted_text)