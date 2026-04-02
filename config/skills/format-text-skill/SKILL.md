---
name: format-text-skill
description: 通过删除多余空格、修正大小写和纠正标点符号来格式化和清理文本内容
---

# 文本格式化器
当被要求格式化文本时:
1. 删除多余空格（将多个空格替换为单个空格）
2. 修正大小写（句子首字母大写）
3. 纠正标点符号（确保正确的结束标点）
4. 返回处理后的文本

## 示例
**输入**: "hello   world"
**输出**: "Hello world."

**输入**: "this is  a    test"
**输出**: "This is a test."


## 可用脚本
### scripts/format_text.py