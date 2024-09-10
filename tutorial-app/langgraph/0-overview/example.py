from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import sys
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.dirname(cur_dir))
sys.path.append(dir_path)

import utils
import llm
from IPython.display import Image, display

@tool
def search(query: str):
    """
    根据查询字符串返回天气信息。

    该函数检查输入的查询字符串是否包含"sf"或"san francisco"（不区分大小写）。
    如果包含，则返回旧金山的天气状况为"60度，有雾"；
    否则，返回默认天气状况"70度，晴朗"。

    参数:
    query (str): 查询字符串，用于判断是否匹配特定的关键词。

    返回:
    str: 描述天气状况的字符串。
    """
    # 检查查询字符串中是否包含"sf"或"san francisco"，不区分大小写
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "it's 60 degrees and foggy"
    return "it's 70 degrees and sunny"

## load config
config_path = os.path.join(dir_path, "config.yaml")
yml_config = utils.load_config(config_path)

## get llm 
llm_model = llm.LLM(yml_config).get_llm()

# 定义一个工具列表，初始包含一个名为search的工具
tools = [search]

# 绑定工具节点到LLM模型，使得模型可以调用工具节点中的工具
model = llm_model.bind_tools(tools=tools)

# 创建一个工具节点，将之前定义的工具列表作为参数传递
tool_node = ToolNode(tools)



def should_continue(state: MessagesState) -> Literal["tools", END]:
    """
    根据当前消息状态决定机器人下一步是否应该继续处理或结束会话。
    
    参数:
    - state: MessagesState类型，表示消息的当前状态，包含消息历史等信息。
    
    返回:
    - Literal["tools", END]: 返回"tools"表示需要机器人继续处理，如调用工具；
    返回END表示机器人结束当前会话，不再处理。
    """
    # 从状态中提取所有消息
    messages = state["messages"]
    if not messages:
        return END
    # 获取最新的一条消息
    last_message = messages[-1]
    # 检查最新消息是否有工具调用
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    """
    调用模型进行回复生成。

    此函数从给定的状态中提取消息列表，并使用预训练的语言模型对这些消息进行处理，
    生成模型的响应。主要用于在对话系统中获取模型对输入消息的回复。

    参数:
    - state: MessagesState 类型，表示当前会话的状态，包含消息列表。

    返回值:
    - 一个包含单个消息的列表，该消息是模型对输入消息的响应。
    """
    # 从状态中提取消息列表
    messages = state["messages"]

    # 使用语言模型处理消息并生成响应
    response = model.invoke(messages)

    # 返回包含模型响应的消息列表
    return {"messages": [response]}

# 创建一个工作流，用于处理对话
workflow = StateGraph(MessagesState)

# 添加图的节点
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# 添加图的边及条件边
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# 创建一个检查点，用于保存对话状态
checkpointer = MemorySaver()

#  编译工作流，生成一个可执行的应用程序
app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": 111}}
final_state = app.invoke(
    {"messages": [HumanMessage(content="what's the weather like in san francisco?")]},
    config=config,
)

print(final_state["messages"][-1].content)

final_state = app.invoke(
    {"messages": [HumanMessage(content="what about shanghai?")]},
    config=config,
)

print(final_state["messages"][-1].content)
