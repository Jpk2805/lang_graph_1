from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int 
    operation: str
    number2: int
    final_number: int

def adder(state: AgentState) -> AgentState:
    """ this is node will add two numbers """
    state['final_number'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """ this is node will subtract two numbers """
    state['final_number'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> AgentState:
    """ in this node we will determine which operation to perform """

    if state['operation'] == '+':
        return "adder"
    elif state['operation'] == '-':
        return "subtractor"
    else:
        raise ValueError("Unknown operation")

graph = StateGraph(AgentState) 

graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)
graph.add_node("decide_next_node", lambda state: state)

graph.add_edge(START, "decide_next_node")

graph.add_conditional_edges(
    "decide_next_node" ,
    decide_next_node,
    {
        "adder": "adder",
        "subtractor": "subtractor"
    }
)

graph.add_edge("adder", END)
graph.add_edge("subtractor", END)

app = graph.compile()

result = app.invoke({
    "number1": 10,
    "operation": "+",
    "number2": 5
})
print(f"Result of addition: {result['final_number']}")
result = app.invoke({
    "number1": 10,
    "operation": "-",
    "number2": 5
})
print(f"Result of subtraction: {result['final_number']}")
