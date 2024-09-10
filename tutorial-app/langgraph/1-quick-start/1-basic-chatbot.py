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
from IPython.display import Image, display

## load config
config_path = os.path.join(dir_path, "config.yaml")
yml_config = utils.load_config(config_path)

## get llm 
llm_model = llm.LLM(yml_config).get_llm()


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_model.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
