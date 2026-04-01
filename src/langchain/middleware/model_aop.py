from typing import Any

from langchain.agents import AgentState
from langchain.agents.middleware import before_model, after_model
from langchain_core.messages import AIMessage
from langgraph.runtime import Runtime


@before_model
def before_model_aop(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    _messages = state["messages"]
    print(f"before model-->")
    for message in _messages:
        print(message)

    if len(_messages) >= 10:
        return {
            "messages": _messages[AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None


@after_model
def after_model_aop(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"after model<--{state['messages'][-1].content}")
    return None
