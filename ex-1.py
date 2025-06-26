from typing import List, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): 
    message: str

def greeting_node(state: AgentState) -> AgentState:
    ''' Simple node that does the greeting to the user. '''

    state['message'] = "hello " + state['message'] + ", hope you are doing well!"
    return state

graph = StateGraph(AgentState)
graph.add_node("greet", greeting_node)
graph.set_entry_point("greet")
graph.set_finish_point("greet")

app = graph.compile()
result = app.invoke({"message": "jay"})

print(result["message"])


from IPython.display import Image, display
display(Image(app.get_graph().draw_png(), width=500, height=500))