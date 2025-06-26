from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random

class AgentState(TypedDict):
    number: List[int]
    counter: int

def guessing_node(state: AgentState) -> AgentState:
    """This node generates a random number and adds it to the list."""
    state['number'].append(random.randint(1, 10))
    
    return state

def check_guess_node(state: AgentState) -> AgentState:
    """This node checks if the counter has reached 5."""

    if state['number'][-1] == 7:
        return "exit"
    else:
        return "guessing_node"
    
graph = StateGraph(AgentState)
graph.add_node("guessing_node", guessing_node)
graph.add_edge(START, "guessing_node")
graph.add_conditional_edges(
    "guessing_node",
    check_guess_node,
    {
        "guessing_node": "guessing_node",
        "exit": END
    }
)

graph.set_entry_point("guessing_node")
app = graph.compile()
result = app.invoke({
    "number": [],
    "counter": 0
})

print(result["number"])