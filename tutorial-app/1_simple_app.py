import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 设置 langchain 环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()

# 设置 openai 环境变量
os.environ["OPENAI_API_KEY"] = getpass.getpass()


model = ChatOpenAI(
    model_name="gpt-4o-mini", 
    openai_api_base="https://api.chatanywhere.tech"
)

system_template = """
Translate the following from into {language}:
"""

# 设置 prompt 模板  
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)

# 设置 prompt 模板参数  
result = prompt_template.invoke({
    "language": "Chainese",
    "text": "What's the future of bitcoin?"
})

# 调用模型
response = model.invoke(result)

print(response)

