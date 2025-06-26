from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int
    final: str

def greeting_node(state: AgentState) -> AgentState:
    """ this is first node of our sequence"""
    state['final'] = f'Hello {state["name"]}'
    state['counter'] = 0
    
    return state

def random_number_node(state: AgentState) -> AgentState:
    """ this node generates a random number and adds it to the list"""
    state['number'].append(random.randint(1, 10))
    state["counter"] += 1

    return state

def check_counter_node(state: AgentState) -> AgentState:
    """ this node checks if the counter has reached 5"""
    if state['counter'] < 5:
        print("Entering random_number_node")
        return "random_number_node"
    else:
        return "exit"
    
graph = StateGraph(AgentState)


graph.add_node("greeting_node", greeting_node)
graph.add_node("random_node", random_number_node)
graph.add_edge("greeting_node", "random_node")

graph.add_conditional_edges(
    "random_node",
    check_counter_node,
    {
        "random_number_node": "random_node",
        "exit": END
    }
)

graph.set_entry_point("greeting_node")

app = graph.compile()

result = app.invoke({
    "name": "John",
    "number": [],
    "counter": 0,
    "final": ""
})

print(result["final"])