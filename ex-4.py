from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List

class AgentState(TypedDict):
    num1: int
    num2: int
    op1: str
    num3: int
    num4: int
    op2: str
    final1: int
    final2: int

def adder(state: AgentState) -> AgentState:
    """ this is first node of our sequence"""
    state['final1'] = state['num1'] + state['num2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """ this is second node of our sequence"""
    state['final1'] = state['num3'] - state['num4']
    return state


def decide_next_node(state: AgentState) -> AgentState:
    """ in this node we will determine which operation to perform """
    if state['op1'] == '+':
        return "adder"
    elif state['op1'] == '-':
        return "subtractor"
    else:
        raise ValueError("Unknown operation")
    
graph = StateGraph(AgentState)
graph.add_node("adder1", adder)
graph.add_node("subtractor1", subtractor)
graph.add_node("decide_next_node", lambda state: state)
graph.add_edge("adder2", adder)
graph.add_edge("subtractor2", subtractor)


graph.add_edge(START, "decide_next_node")
graph.add_conditional_edges(
    "decide_next_node",
    decide_next_node,
    {
        "adder1": "adder1",
        "subtractor1": "subtractor1"
    }
)
graph.add_edge("next_add", END)

