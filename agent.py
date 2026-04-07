from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools import calculate_budget, search_flights, search_hotels

load_dotenv()

HISTORY_FILE = Path("history/chat_history.json")
SYSTEM_PROMPT_FILE = Path("system_prompt.txt")


def load_system_prompt() -> str:
    if not SYSTEM_PROMPT_FILE.exists():
        raise FileNotFoundError(
            "Không tìm thấy file system_prompt.txt. "
            "Hãy tạo file này trước khi chạy agent."
        )
    return SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = load_system_prompt()


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


tools_list = [search_flights, search_hotels, calculate_budget]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools_list)


def reset_history_file() -> None:
    """
    Mỗi lần chạy lại chương trình, ghi đè history cũ.
    """
    HISTORY_FILE.write_text("[]", encoding="utf-8")


def message_to_dict(msg: BaseMessage) -> dict[str, Any]:
    data: dict[str, Any] = {
        "type": msg.__class__.__name__,
        "content": msg.content,
    }

    additional_kwargs = getattr(msg, "additional_kwargs", None)
    if additional_kwargs:
        data["additional_kwargs"] = additional_kwargs

    response_metadata = getattr(msg, "response_metadata", None)
    if response_metadata:
        data["response_metadata"] = response_metadata

    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        data["tool_calls"] = tool_calls

    if isinstance(msg, ToolMessage):
        data["tool_call_id"] = msg.tool_call_id
        data["name"] = getattr(msg, "name", None)

    return data


def save_history(messages: list[BaseMessage]) -> None:
    serializable = [message_to_dict(msg) for msg in messages]
    HISTORY_FILE.write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def ensure_system_message(messages: list[BaseMessage]) -> list[BaseMessage]:
    if messages and isinstance(messages[0], SystemMessage):
        return messages
    return [SystemMessage(content=SYSTEM_PROMPT)] + messages


def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
    messages = ensure_system_message(state["messages"])
    response = llm_with_tools.invoke(messages)

    print("\n[AGENT LOG]")
    if getattr(response, "tool_calls", None):
        for tool_call in response.tool_calls:
            print(f"- Gọi tool: {tool_call['name']}({tool_call['args']})")
    else:
        print("- Không gọi tool, trả lời trực tiếp.")

    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)
builder.add_edge("tools", "agent")

graph = builder.compile()


def get_last_ai_message(messages: list[BaseMessage]) -> AIMessage | None:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            return msg
    return None


if __name__ == "__main__":
    print("=" * 70)
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print("History lưu tại: history/chat_history.json")
    print("Gõ 'quit' để thoát")
    print("=" * 70)

    reset_history_file()

    chat_history: list[BaseMessage] = []

    while True:
        user_input = input("\nBạn: ").strip()

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Tạm biệt bạn nhé!")
            break

        if not user_input:
            print("TravelBuddy: Bạn cứ nhập nhu cầu của mình, mình sẽ hỗ trợ nhé.")
            continue

        chat_history.append(HumanMessage(content=user_input))

        try:
            result = graph.invoke({"messages": chat_history})
            full_messages = result["messages"]

            final_ai_message = get_last_ai_message(full_messages)
            if final_ai_message is not None:
                print(f"\nTravelBuddy: {final_ai_message.content}")
                chat_history = full_messages
            else:
                fallback = (
                    "Mình chưa tạo được phản hồi phù hợp. "
                    "Bạn thử diễn đạt rõ hơn một chút nhé."
                )
                print(f"\nTravelBuddy: {fallback}")
                chat_history.append(AIMessage(content=fallback))

        except Exception as exc:
            print(f"\n[ERROR LOG] {exc}")
            error_message = "Xin lỗi, mình đang gặp sự cố khi xử lý yêu cầu của bạn. Bạn hãy thử lại nhé."
            print(f"\nTravelBuddy: {error_message}")
            chat_history.append(AIMessage(content=error_message))

        save_history(chat_history)