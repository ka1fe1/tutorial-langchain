from langchain_openai import ChatOpenAI
import getpass
import os


class LLM:
    def __init__(self, config: dict):
        self.config = config

    def get_llm(self) -> ChatOpenAI:
        # set langchain tracing
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = self.config["langchain"]["api_key"]

        model = ChatOpenAI(
            model_name="gpt-4o-mini", 
            openai_api_base=self.config["open_ai"]["api_base"],
            openai_api_key=self.config["open_ai"]["api_key"]
        )
        return model