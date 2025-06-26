from typing import TypedDict, Sequence, Annotated
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "List of messages"]

@tool
def update(content: str) -> str:
    """Updates the document with the provided content."""

    global document_content
    document_content += f"\n{content}"

    return f"Document has been updated. The current content is {document_content}"  

@tool
def save(filename: str) -> str:
    """Saves the document content to a text file.
    
    Args:
        filename: Name for the text file.

    """
    
    global document_content
    with open(filename, "w") as file:
        file.write(document_content)

    if filename.endswith(".txt"):
        filename = f"{filename}.txt"

    try: 
        with open(filename, "w") as file:
            file.write(document_content)
        print(f"Document saved as {filename}")
    except Exception as e:
        print(f"Error saving document: {e}")
        return f"Error saving document: {e}"
    
    return "Document has been saved."

tools = [update, save]

model = ChatOpenAI(model="gpt-4o", tools=tools).bind_tools(tools)

def our_agent(state:AgentState)->AgentState:
    system_prompt = SystemMessage(
        content=f"""You are a Drafter, a helpful AI assistant that can draft documents based on user input. 
        You can update the document with new content or save it to a file. 
        Use the tools provided to perform these actions. 
        Always show the current document content after each update or save operation. 
        
        The current content is : {document_content}."""
    )

    if not state['messages']:
        user_input = "I'm ready to draft a document. Please provide the content."
        user_message = HumanMessage(content=user_input)
    else: 
        user_input = input("\nWhat would you like to do to the document? ")
        print(f"You: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state['messages']) + [user_message]


    response = model.invoke(all_messages)

    print(f"AI: {response.content}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_message = ToolMessage(
            name=response.tool_calls[0].name,
            args=response.tool_calls[0].args
        )
        all_messages.append(tool_message)
        print(f"Tool called: {tool_message.name} with args: {tool_message.args}")


    return { "messages": list(state['messages']) + [user_message, response] }

def should_continue(state: AgentState) -> str:
    """This node will determine if the conversation should continue."""
    message = state['messages']

    if not message:
        return "continue"
    
    for message in reversed(message):
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and 
            "document" in message.content.lower()):
            return "end"
        

    return "continue"

graph = StateGraph(AgentState)

graph.add_node("our_agent", our_agent)
tool_node = ToolNode(tools=tools)
graph.add_node("tool", tool_node)

graph.set_entry_point("our_agent")
graph.add_edge("our_agent", "tool")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "our_agent",
        "end": END
    }
)

app = graph.compile()

print("Welcome to the Document Drafting Agent!")
document_content = ""
user_input = input("You: ")
while user_input.lower() != "exit":
    result = app.invoke({
        "messages": [],
    })

    print(f"AI: {result['messages'][-1].content}")
    
    user_input = input("You: ")
    while user_input.lower() != "exit":
        result = app.invoke({
            "messages": [],
        })

        print(f"AI: {result['messages'][-1].content}")
        user_input = input("You: ")
