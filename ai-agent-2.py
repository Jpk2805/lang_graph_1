import os
from typing import List, Dict, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
    response: str

llm = ChatOpenAI(model="gpt-4o") 

def process(state: AgentState) -> AgentState:
    """this node will solve the request of the user"""

    response = llm.invoke(state['messages'])

    state['messages'].append(AIMessage(content=response.content))

    print(f"AI: {response.content}")

    return state

graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []
user_input = input("You: ")

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))

    result = agent.invoke({
        "messages": conversation_history
    })
    conversation_history = result['messages']
    user_input = input("You: ")