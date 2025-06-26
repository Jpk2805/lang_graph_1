from typing import List, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:

    """ this function handles multiple different values as input and returns a string."""

    state['result'] = f"hi there {state['name']}, your sum is = {sum(state['values'])}"

    return state

graph = StateGraph(AgentState)

graph.add_node("process_values", process_values)

graph.set_entry_point("process_values")
graph.set_finish_point("process_values")

app = graph.compile()
answer = app.invoke({
    "values": [1, 2, 3, 4, 5],
    "name": "jay"
})

print(answer["result"])

from IPython.display import Image, display
display(Image(app.get_graph().draw_png(), width=500, height=500))