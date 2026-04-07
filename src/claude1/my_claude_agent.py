import os

import click

from src.claude1.react_agent import ReActAgent
from src.claude1.tools import read_file, write_to_file, run_terminal_command


@click.command()
@click.argument('project_directory', type=click.Path(file_okay=False, dir_okay=True))
def main(project_directory):
    # 确保项目目录存在，如果不存在则创建
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    project_dir = os.path.abspath(project_directory)

    tools = [read_file, write_to_file, run_terminal_command]
    agent = ReActAgent(tools=tools, model="deepseek-chat", project_directory=project_dir)

    task = input("请输入任务：")

    final_answer = agent.run(task)

    print(f"\n\n✅ Final Answer：{final_answer}")


# python -m my_claude_agent.my_claude_agent test
# uv run -m my_claude_agent.my_claude_agent test
# snake是参数，表示我们本次任务生成的代码会放在 test 这个新建的目录之下
# 输入任务：写一个贪吃蛇游戏，使用HTML，css和js实现，代码分别放在不同的文件中。
if __name__ == "__main__":
    main()
