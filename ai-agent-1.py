from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]
    response: str

llm = ChatOpenAI(model="gpt-4o")

def process(state:AgentState) -> AgentState:
    response = llm.invoke(state['messages'])

    print(f"Response: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.set_entry_point("process")
graph.set_finish_point("process")
app = graph.compile()

user_input = input("Enter your messages: ")

Result = app.invoke({
    "messages": [
        HumanMessage(content=user_input)
    ],
    "response": ""
})
