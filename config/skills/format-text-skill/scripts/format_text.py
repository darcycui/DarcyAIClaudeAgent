# scripts/process.py
import sys


def format_text(text):
    """格式化文本"""
    print('原始文本：', text)
    # 删除多余空格
    text = ' '.join(text.split())
    # 首字母大写
    text = text.capitalize()
    # 添加句号（如果缺失）
    if not text.endswith(('.', '!', '?')):
        text += '.'
    print('格式化后的文本：', text)
    return text

if __name__ == '__main__':
    # 解析命令行参数 得到输入文本 text
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
    else:
        raise ValueError('请提供要处理的文本')
    formatted_text = format_text(input_text)
    print(formatted_text)