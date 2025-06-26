from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    name: str
    values: list
    operation: str
    result: str

def process_node(state:AgentState)-> AgentState:
    """ This node will process the values and prform the operation specified in the state. """
    if state['operation'] == 'sum':
        state['result'] = sum(state['values'])
    elif state['operation'] == 'product':
        product = 1
        for value in state['values']:
            product *= value
        state['result'] = product
    else:
        state['result'] = 'Unknown operation'

    state['result'] = f"Hello {state['name']}, the result of {state['operation']} is: {state['result']}"
    
    return state

graph = StateGraph(AgentState)
graph.add_node("math_operator", process_node)
graph.set_entry_point("math_operator"
                      )
graph.set_finish_point("math_operator")

app = graph.compile()

result = app.invoke({"name": "John", "values": [1, 2, 3], "operation": "sum"})

print(result['result'])