from langchain_community.tools.tavily_search import TavilySearchResults
import utils
import llm
import os
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.yaml")
yml_config = utils.load_config(config_path)

llm = llm.LLM(yml_config)
model = llm.get_llm()

memory = MemorySaver()

## 设置 agent 的工具
os.environ["TAVILY_API_KEY"] = yml_config["tavily"]["api_key"]
search = TavilySearchResults(max_results=2)
tools = [search]

## 设置 agent 的 prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can search the web for information. answer questions in {language}"),
    ("human", "{human}"),
])

## 创建 agent
agent_executor = create_react_agent(model=model, tools=tools, checkpointer=memory)

chain = prompt | agent_executor

## 设置 agent 的内存和状态管理
config = {"configurable": {"thread_id": "abc123"}}

## 运行 agent
for chunk in chain.stream(
    {"language": "Chinese", "human": "i live in Shanghai"}, 
    config=config,
):
    print(chunk)
    print("----")


for chunk in chain.stream(
    {"language": "Chinese", "human": "我居住地的天气是怎样的"}, 
    config=config,
):
    print(chunk)
    print("----")




