import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

os.environ["OPENAI_API_KEY"] = "sk-glsafgZfTBhlzlWR95JNAkYSO6vdsTBE7Proh3tgM0WnLZuf"

model = ChatOpenAI(
    model_name="gpt-4o-mini", 
    openai_api_base="https://api.chatanywhere.tech"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability in {language}."),
    MessagesPlaceholder(variable_name="messages"),
 ])

# RunnableWithMessageHistory 参数及用法说明

# 1. chain: 要运行的链或可运行对象
# 这是处理输入并生成输出的核心组件

# 2. get_session_history: 函数，接收 session_id 并返回 BaseChatMessageHistory 对象
# 用于存储和检索特定会话的消息历史
# 在本文件中，已经定义了 get_session_history 函数

# 3. input_messages_key: 字符串，指定输入字典中包含消息的键名
# 告诉 RunnableWithMessageHistory 在哪里找到新的输入消息

# 4. history_messages_key: 可选，字符串，指定输出字典中存储历史消息的键名
# 如果不指定，历史消息将直接添加到输入消息中

# 5. output_messages_key: 可选，字符串，指定输出字典中存储新生成消息的键名
# 如果不指定，新消息将直接添加到历史消息中

# 示例用法：
# with_message_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="messages",
#     history_messages_key="history",
#     output_messages_key="output"
# )

# 这些参数允许灵活地控制消息的输入、历史管理和输出，
# 以确保在多个会话中有效地管理对话历史，提供连贯和上下文相关的响应。


def prompt_template(session_id: str):
    chain = prompt | model 

    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

    language = "Chinese"

    config = {
        "configurable": {
            "session_id": session_id
        },
    }

        # Example conversation
    human_messages = [
        "请阐述一下黄金的投资价值",
        "My name is tataka1",
        "What is my name?",
        "What's answer of first question?"
    ]

    for message in human_messages:
        response = with_message_history.invoke(
            {"messages": [HumanMessage(content=message)], "language": language},
            config=config,
        )
        print(f"Human: {message}")
        print(f"AI: {response.content}\n")

# trim_messages 的作用及其参数含义

# trim_messages 用于管理和修剪对话历史，以保持对话的清晰度和相关性。
# 它通过控制历史消息的长度和内容来优化对话上下文。

# 参数解释：
# 1. max_tokens: 设置消息历史的最大令牌数，控制历史长度。
#    例如：max_tokens=1000 限制历史最多包含1000个令牌。

# 2. strategy: 定义如何修剪消息。常用策略：
#    - "last": 保留最近的消息，删除较早的消息。
#    - "first": 保留最早的消息，删除较新的消息。

# 3. token_counter: 用于计算消息中令牌数的函数或对象。
#    通常使用语言模型来执行此操作。

# 4. include_system: 布尔值，决定是否在修剪过程中包含系统消息。
#    True 表示包含系统消息，False 则排除。

# 5. allow_partial: 布尔值，决定是否允许部分消息被保留。
#    False 时只保留完整的消息，True 允许保留部分消息。

# 6. start_on: 指定从哪种类型的消息开始保留。
#    例如，"human" 表示从人类消息开始保留。

# 这些参数允许灵活地控制如何修剪和管理对话历史，
# 确保保留最相关的信息，同时保持历史的简洁性和效率。

def managing_conversation_history():
    trimmer = trim_messages(
        max_tokens=1000,
        strategy="last",
        token_counter=model,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    history_messages = [
        SystemMessage(content="you're a good assistant"),
        HumanMessage(content="hi! I'm bob"),
        AIMessage(content="hi!"),
        HumanMessage(content="I like vanilla ice cream"),
        AIMessage(content="nice"),
        HumanMessage(content="whats 2 + 2"),
        AIMessage(content="4"),
        HumanMessage(content="thanks"),
        AIMessage(content="no problem!"),
        HumanMessage(content="having fun?"),
        AIMessage(content="yes!"),
    ]

    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
        | prompt
        | model
    )

    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

    config = {
        "configurable": {
            "session_id": "123"
        },
    }

    response = with_message_history.invoke({
        "messages": history_messages +[HumanMessage(content="外企在上海没有办公地点对于个人有什么影响？")],
        "language": "Chinese",
    }, config=config)

    print(response.content)

    response = with_message_history.invoke(
        {"messages": [HumanMessage(content="what last math question and last question did i ask? and what's my name?")], "language": "Chinese"},
        config=config,
    )

    print(response.content)


if __name__ == "__main__":
    # prompt_template("123")
    managing_conversation_history()





