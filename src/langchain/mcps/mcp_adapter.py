import asyncio
import json
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_mcp_tools(config_path: str = None) -> list:
    """获取 MCP Server 的所有工具"""
    # 加载配置文件
    mcp_config = load_mcp_config(config_path)
    # 解析服务器配置
    servers = parse_servers_from_config(mcp_config)
    print(f"已加载 MCP Servers: {list(servers.keys())}")
    # 创建客户端并获取工具
    client = MultiServerMCPClient(servers)
    # 异步方式获取工具
    tools = await client.get_tools()
    print(f"共获取到 {len(tools)} 个 MCP 工具:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    return tools


def load_mcp_config(config_path: str = None) -> dict:
    """加载 MCP Server 配置文件"""
    if config_path is None:
        # 默认使用项目根目录的配置文件
        config_path = Path(__file__).parent.parent.parent.parent / "config" / "mcp_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_servers_from_config(mcp_config: dict) -> dict:
    """解析 MCP 配置，转换为 MultiServerMCPClient 需要的格式"""
    servers = {}
    for server_name, server_config in mcp_config.get("mcpServers", {}).items():
        if server_config.get("disabled", False):
            continue
        servers[server_name] = {
            "transport": server_config.get("type", "stdio"),
            "command": server_config.get("command"),
            "args": server_config.get("args", []),
            # "timeout": server_config.get("timeout", 60), # 不支持设置 timeout
        }
    return servers