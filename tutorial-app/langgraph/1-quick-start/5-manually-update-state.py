from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
import sys
import os
import json

cur_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.dirname(cur_dir))
sys.path.append(dir_path)

import utils
import llm
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, ToolMessage


## load config
config_path = os.path.join(dir_path, "config.yaml")
yml_config = utils.load_config(config_path)

## get llm 
llm_model = llm.LLM(yml_config).get_llm()

class State(TypedDict):
    messages: Annotated[list, add_messages]


os.environ["TAVILY_API_KEY"] = yml_config["tavily"]["api_key"]
tool = TavilySearchResults(max_results=2)
tools = [tool]

llm_with_tools = llm_model.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

tool_node = ToolNode(tools=tools)

workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

workflow.set_entry_point("chatbot")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer, interrupt_before=["tools"])

print(f"graph style: {graph.get_graph().draw_mermaid()}")

config = {"configurable": {"thread_id": "2"}}    
user_input = "What are the benefits of LangGraph?"
events = graph.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]

print("-------------------------------------------------")

new_tool_call = existing_message.tool_calls[0].copy()
new_tool_call["args"]["query"] = "langgraph 的 human in loop 是什么意思"
new_messages = AIMessage(
    content=existing_message.content,
    tool_calls=[new_tool_call],
    id= existing_message.id
)

graph.update_state(
    config=config,
    values={"messages": [new_messages]}
)
next = graph.get_state(config).next
print(f"===next node===: {next}")
# graph.get_state(config).values["messages"][-1].tool_calls

print(f"===tool calls===: {graph.get_state(config).values['messages'][-1].tool_calls}")

events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

