import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import utils

# 获取当前文件所在目录路径，模拟 __DIR__
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建相对路径
config_file_path = os.path.join(current_dir, 'config.yaml')


yml_config = utils.load_config(config_file_path)

# 设置 langchain 环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = yml_config["langchain"]["api_key"]


model = ChatOpenAI(
    model_name="gpt-4o-mini", 
    openai_api_base=yml_config["open_ai"]["api_base"],
    openai_api_key=yml_config["open_ai"]["api_key"]
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

