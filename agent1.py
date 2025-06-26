from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, START


class AgentState(TypedDict):
    message : str

def greating_node(state: AgentState) -> AgentState:
    """"Simple node that adds a greeting message to the state."""

    state['message'] = 'hey ' + state['message'] + ', how is your day?'

    return state


graph = StateGraph(AgentState)

graph.add_node("greeter", greating_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({
    "message": "jay"})

print(result["message"])

from IPython.display import Image, display
display(Image(app.get_graph().draw_png(), width=500, height=500))