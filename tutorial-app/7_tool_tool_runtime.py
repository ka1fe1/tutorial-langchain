import os
import utils
import llm

from typing import List
from langchain_core.tools import tool, InjectedToolArg
from typing_extensions import Annotated
from langchain_core.messages import HumanMessage

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "config.yaml")
yml_config =utils.load_config(config_path)

llm_model = llm.LLM(yml_config).get_llm()

user_to_pets = {}

@tool(parse_docstring=True)
def update_favorite_pets(pets: List[str], user_id: Annotated[str, InjectedToolArg]) -> None:
    """Add the list of favorite pets.
    
    Args:
        pets: List of favorite pets
        user_id: The ID of the user to update the favorite pets for
    """
    user_to_pets[user_id] = pets

@tool(parse_docstring=True)
def delete_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """Delete the list of favorite pets.

    Args:
        user_id: User's ID.
    """
    if user_id in user_to_pets:
        del user_to_pets[user_id]


@tool(parse_docstring=True)
def list_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """List favorite pets if any.

    Args:
        user_id: User's ID.
    """
    return user_to_pets.get(user_id, [])


print(f"input schema:\n {update_favorite_pets.get_input_schema().schema()}\n {'='*100}")
print(f"tool call schema:\n {update_favorite_pets.tool_call_schema.schema()}\n {'='*100}")

tools = [update_favorite_pets, delete_favorite_pets, list_favorite_pets]
tools_map = {tool.name: tool for tool in tools}

llm_with_tools = llm_model.bind_tools(tools)

messages = [HumanMessage(content="my favorite animals are cats and parrots")]
ai_msg = llm_with_tools.invoke(messages)
print(f"ai_msg:\n {ai_msg}\n {'='*100}")

messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    tool = tools_map[tool_call["name"].lower()]
    tool_call["args"]["user_id"] = "123"
    tool_response = tool.invoke(tool_call["args"])
    messages.append(tool_response)

print(f"messages:\n {messages}\n {'='*100}")

print(f"user_to_pets:\n {user_to_pets}\n {'='*100}")

# updated_ai_msg = llm_with_tools.invoke(messages)
# print(f"updated_ai_msg:\n {updated_ai_msg}\n {'='*100}")
