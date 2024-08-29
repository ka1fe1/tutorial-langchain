# Vector Store And Retrievers
- [Vector Store And Retrievers](#vector-store-and-retrievers)
  - [Vector Store](#vector-store)
  - [Retrievers](#retrievers)

## Vector Store

向量存储（Vector Store）是一种用于存储和检索高维向量数据的专门数据库系统。

Vector Store 的作用是，可用于存储和检索非结构化数据，如文本、图像等。


## Retrievers

Retrievers（检索器）是在向量存储或其他数据源中检索相关信息的组件。它们的主要作用是根据给定的查询或问题，从大量数据中快速找出最相关的信息。

Retrievers 的主要功能和作用包括：

1. 相似性搜索：基于查询的语义或内容，在向量空间中找出最相似的文档或片段。

2. 上下文提供：为大语言模型（LLMs）提供相关的上下文信息，以生成更准确和相关的回答。

3. 信息过滤：从大量数据中筛选出最相关的部分，减少噪音和不相关信息。

4. 效率提升：通过快速检索相关信息，提高整个问答或信息检索系统的效率。

5. 知识增强：允许模型访问存储在外部数据源中的额外知识，扩展其回答能力。

在 LangChain 中，Retrievers 通常与向量存储（如 Chroma）结合使用，形成强大的检索增强生成（RAG）系统。这种系统能够显著提高大语言模型处理特定领域问题或需要最新信息的能力。
