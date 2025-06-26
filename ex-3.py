from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    final: str


def first_node(state: AgentState) -> AgentState:
    """ this is first node of our sequence"""

    state['final'] = f'hello {state["name"]}'

    return state

def second_node(state: AgentState) -> AgentState:
    """ this is second node of our sequence"""

    state['final'] += f', you are {state["age"]} years old'

    return state

def third_node(state: AgentState) -> AgentState:
    """ this is third node of our sequence"""

    state['final'] += f' and your skills are: {", ".join(state["skills"])}'

    return state

graph = StateGraph(AgentState)

graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)

graph.add_edge("first", "second")
graph.add_edge("second", "third")

graph.set_entry_point("first")
graph.set_finish_point("third")

app = graph.compile()

result = app.invoke({"name": "John", "age": 30, "skills": ["Python", "AI", "Data Science"]})
print(result['final'])

