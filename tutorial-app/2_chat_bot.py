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





