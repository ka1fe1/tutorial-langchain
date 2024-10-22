import os
import utils
import llm
from langchain_core.tools import tool

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "config.yaml")
yml_config =utils.load_config(config_path)

from langchain_core.messages import HumanMessage

llm_model = llm.LLM(yml_config).get_llm()

@tool(parse_docstring=True)
def add(a: int, b: int) -> int:
    """Add two numbers
    
    Args:
        a: First integer
        b: Second integer

    Returns:
        int: the sum of a and b
    """
    return a + b

@tool(parse_docstring=True)
def mul(a: int, b: int) -> int:
    """Multiply two numbers
    
    Args:
        a: First integer
        b: Second integer

    Returns:
        int: the product of a and b
    """
    return a * b

tools = [add, mul]
tools_dict = {tool.name: tool for tool in tools}

llm_with_tools = llm_model.bind_tools(tools)

query = "What is 3 * 12 and 3 + 12?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)

print(f"ai_msg:\n {ai_msg}")
print("-"*100)

messages.append(ai_msg)
for tool_call in ai_msg.tool_calls:
    tool = tools_dict[tool_call["name"].lower()]
    tool_msg = tool.invoke(tool_call)
    messages.append(tool_msg)

print(f"messages:\n {messages}")
print("-"*100)

# Re-invoke LLM with updated messages
updated_ai_msg = llm_with_tools.invoke(messages)

print(f"Updated ai_msg:\n {updated_ai_msg}")
print("-" * 100)



