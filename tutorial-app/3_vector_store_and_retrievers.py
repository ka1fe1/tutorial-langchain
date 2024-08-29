import utils
from llm import LLM
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.runnables.base import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough



# 获取当前文件所在目录路径，模拟 __DIR__
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建相对路径
config_file_path = os.path.join(current_dir, 'config.yaml')


yml_config = utils.load_config(config_file_path)


llm = LLM(yml_config)
model = llm.get_llm()

documents = [
        Document(
            page_content="Dogs are great companions, known for their loyalty and friendliness.",
            metadata={"source": "mammal-pets-doc"},
        ),
        Document(
            page_content="Cats are independent pets that often enjoy their own space.",
            metadata={"source": "mammal-pets-doc"},
        ),
        Document(
            page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
            metadata={"source": "fish-pets-doc"},
        ),
        Document(
            page_content="Parrots are intelligent birds capable of mimicking human speech.",
            metadata={"source": "bird-pets-doc"},
        ),
        Document(
            page_content="Rabbits are social animals that need plenty of space to hop around.",
            metadata={"source": "mammal-pets-doc"},
        ),
    ]


def vector_store():

    embeddings = OpenAIEmbeddings(
        openai_api_key=yml_config["open_ai"]["api_key"],
        openai_api_base=yml_config["open_ai"]["api_base"],
        model="text-embedding-3"
    )

    vector_store = Chroma.from_documents(
        documents,
        embedding=embeddings,
    )
    
    vector_store.asimilarity_search_with_score("cat")

    # print(response)

def retrievers():
    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(
            openai_api_key=yml_config["open_ai"]["api_key"],
            openai_api_base=yml_config["open_ai"]["api_base"],
            model="text-embedding-3"
        ),
        persist_directory="vector_store"
    )
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1}
    )

    message = """
        Answer this question using the provided context only.
        {question}
        Context:
        {context}
    """

    promt = ChatPromptTemplate.from_messages(["human", message])

    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | promt | model
    response = rag_chain.invoke("tell me about cats")
    print(response.content)


if __name__ == "__main__":
    # vector_store()
    retrievers()


