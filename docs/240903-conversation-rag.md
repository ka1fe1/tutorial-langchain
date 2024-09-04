# conversation rag

```python
def conversation_rag_chain():
    memory = MemorySaver()

    ## load
    loader = WebBaseLoader(
    web_paths=("https://ka1fe1.github.io/tutorial-langchain/docs/24082902-build-agent.html",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                name="p"
            )
        )    
    )
    docs = loader.load_and_split()
    print(docs)

    ## split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    ## store
    vector_store = Chroma.from_documents(
        splits,
        OpenAIEmbeddings(
            model=yml_config["open_ai"]["api_embeddings_model"],
            openai_api_base=yml_config["open_ai"]["api_embeddings_base"],
            openai_api_key=yml_config["open_ai"]["api_key"],
        ),   
    )
    retriever = vector_store.as_retriever()

    ## retreival
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )
    history_aware_retriever = create_history_aware_retriever(llm_model, retriever, contextualize_q_prompt)

    ## generation
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )
    qa_chain = create_stuff_documents_chain(llm_model, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    config = {"configurable": {"session_id": "abc123"}}
    response = conversational_rag_chain.invoke(
        {"input": "agent 是什么? answer in chinese"},
        config = config,
    )
    print(response["answer"])

    response = conversational_rag_chain.invoke(
        {"input": "what is feature about it? answer in chinese"},
        config = config,
    )
    print(response["answer"])
```