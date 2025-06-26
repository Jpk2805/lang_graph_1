from typing import TypedDict, Sequence, Annotated
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pprint import pprint

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add_numbers(number1: int, number2: int) -> int:
    """Adds two numbers."""
    return number1 + number2

tool = [add_numbers]

model = ChatOpenAI(model="gpt-4o", tools=tool).bind_tools(tool)

def model_call(state: AgentState) -> AgentState:
    """This node will call the model with the messages."""
    system_prompt = SystemMessage(
        content="You are a helpful AI assistant. You can perform calculations using the provided tools."
    )


    response = model.invoke([system_prompt] + state['messages'])
    return {
        "messages": response
    }

def should_continue(state: AgentState):
    """This node will determine if the conversation should continue."""
    last_message = state['messages'][-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "model_call"

graph = StateGraph(AgentState)
graph.add_node("model_call", model_call)

tool_node = ToolNode(tools=tool)

graph.add_node("tool", tool_node)

graph.set_entry_point("model_call")
graph.add_conditional_edges(
    "model_call",
    should_continue,
    {
        "model_call": "tool",
        "end": END
    }
)
graph.add_edge("tool", "model_call")

app = graph.compile()


def print_conversation(stream):
    for message in stream:
        s = message['messages'][-1]
        if isinstance(s, tuple):
            pprint(message)
        else:
            message.pretty_print()


input = {
    "messages": [
    ("user", "What is 2 + 2?"),
]}
print_conversation(app.stream(input, stream_mode="values"))