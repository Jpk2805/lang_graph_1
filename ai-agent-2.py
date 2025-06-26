from typing import TypedDict, Sequence, Annotated
from dotenv import load_dotenv TypedDict, Union
from langchain_core.messages import ToolMessageEND
from langchain_core.messages import BaseMessagee, AIMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pprint import pprintHumanMessage, AIMessage]]
    response: str
load_dotenv()
llm = ChatOpenAI(model="gpt-4o") 
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    """this node will solve the request of the user"""
@tool
def add_numbers(number1: int, number2: int) -> int:
    """Adds two numbers."""
    return number1 + number2(AIMessage(content=response.content))

tool = [add_numbers]ponse.content}")

model = ChatOpenAI(model="gpt-4o", tools=tool).bind_tools(tool)

def model_call(state: AgentState) -> AgentState:
    """This node will call the model with the messages."""
    system_prompt = SystemMessage(
        content="You are a helpful AI assistant. You can perform calculations using the provided tools."
    ).add_edge("process", END)

agent = graph.compile()
    response = model.invoke([system_prompt] + state['messages'])
    return {_history = []
        "messages": response
    }
while user_input != "exit":
def should_continue(state: AgentState):ssage(content=user_input))
    """This node will determine if the conversation should continue."""
    last_message = state['messages'][-1]
    if not last_message.tool_calls:story
        return "end"
    else:rsation_history = result['messages']
        return "model_call": ")graph = StateGraph(AgentState)graph.add_node("model_call", model_call)tool_node = ToolNode(tools=tool)graph.add_node("tool", tool_node)graph.set_entry_point("model_call")graph.add_conditional_edges(    "model_call",    should_continue,    {        "model_call": "tool",        "end": END    })graph.add_edge("tool", "model_call")app = graph.compile()def print_conversation(stream):    for message in stream:        pprint(message)input = {    "messages": [    ("user", "What is 2 + 2?"),]}print_conversation(app.stream(input, stream_mode="values"))