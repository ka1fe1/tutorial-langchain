from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
import sys
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.dirname(cur_dir))
sys.path.append(dir_path)

import utils
import llm
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

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
graph = workflow.compile(checkpointer=checkpointer, interrupt_after=["tools"])

config = {"configurable": {"thread_id": "1"}}


user_input = "I'm learning LangGraph. Could you do some research on it for me?"
config = {"configurable": {"thread_id": "1"}}
# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()


# `None` will append nothing new to the current state, letting it resume as if it had never been interrupted
events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()        