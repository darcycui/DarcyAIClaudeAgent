from typing import Any

from langchain.agents.middleware import before_agent, after_agent
from langgraph.runtime import Runtime


@before_agent
def before_agent_aop(state: dict[str, Any], runtime: Runtime) -> dict[str, Any] | None:
    print(f"before agent-->")
    print(state)

    # # 只在第一次调用时扫描技能
    # if "skills_metadata" not in state:
    #     return {
    #         "skills_metadata": {k: v.to_dict() for k, v in list_available_skills().items()},
    #     }
    return None

@after_agent
def after_agent_aop(state: dict[str, Any], runtime: Runtime) -> dict[str, Any] | None:
    print(f"after agent<--")
    print(state)
    return None