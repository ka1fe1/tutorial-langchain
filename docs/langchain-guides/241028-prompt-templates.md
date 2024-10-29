# Prompt templates
- [Prompt templates](#prompt-templates)
  - [prompt templates introduction](#prompt-templates-introduction)
    - [what is prompt template](#what-is-prompt-template)
    - [how to use prompt template](#how-to-use-prompt-template)
      - [string promptTemplates](#string-prompttemplates)
      - [chatPromptTemplates](#chatprompttemplates)
      - [messagePlaceholder](#messageplaceholder)
  - [how to use few shot examples - `FewShotPromptTemplate`](#how-to-use-few-shot-examples---fewshotprompttemplate)
    - [why need fee shot examples](#why-need-fee-shot-examples)
    - [how to use fee shot examples](#how-to-use-fee-shot-examples)
      - [use a set of examples](#use-a-set-of-examples)
      - [use an example selector](#use-an-example-selector)
  - [how to use few shot example to chat model - `FewShotChatMessagePromptTemplates`](#how-to-use-few-shot-example-to-chat-model---fewshotchatmessageprompttemplates)
    - [use fixed examples](#use-fixed-examples)
    - [use example selector](#use-example-selector)

## prompt templates introduction

### what is prompt template

提示词模版的作用就是将用户的输入和参数转变成指令给到 LLM

### how to use prompt template

#### string promptTemplates

这类提示词模版通常被用于格式化单一的字符串，通常用于简单的输入。

实现要点: 使用 `from_template` 方法来实现
```python
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

prompt_template.invoke({"topic": "cats"})
```

#### chatPromptTemplates

用于格式化一组消息

实现要点: 使用 `ChatPromptTemplate` 类

```python
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

prompt_template.invoke({"topic": "cats"})
```

#### messagePlaceholder

这类提示词模版，用于在指定的地方加入一个消息数组

实现要点: 使用 `ChatPromptTemplate` & `MessagesPlaceholder` 类

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})

# other method
prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{msgs}") # <-- This is the changed part
])
```

## how to use few shot examples - `FewShotPromptTemplate`

使用 `FewShotPromptTemplate` 类

### why need fee shot examples

给 LLM 提供少量的示例，是简单且有效的提升 LLM 表现的方式

### how to use fee shot examples

#### use a set of examples

1. create a formatter for few-shot examples

```python
from langchain_core.prompts import PromptTemplate

example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")
```

2. create example set

```python
examples = [
    {
        "question": "Who lived longer, Muhammad Ali or Alan Turing?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
""",
    },
    {
        "question": "When was the founder of craigslist born?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
    },
    {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball
""",
    }
]
```

3. use `FewShotPromptTemplate`

```python
from langchain_core.prompts import FewShotPromptTemplate

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

print(
    prompt.invoke({"input": "Who was the father of Mary Ball Washington?"}).to_string()
)
```

#### use an example selector

使用 `SemanticSimilarityExampleSelector` 的实例来根据用户输入从示例中选择最相似的示例

```python
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # This is the number of examples to produce.
    k=1,
)

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

print(
    prompt.invoke({"input": "Who was the father of Mary Ball Washington?"}).to_string()
)
```

## how to use few shot example to chat model - `FewShotChatMessagePromptTemplates`

使用 `FewShotChatMessagePromptTemplates` 类来实现给聊天机器人提供一些简单示例

### use fixed examples

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]

# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | model

chain.invoke({"input": "What is 2 🦜 9?"})
```

### use example selector

```python
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
    {"input": "2 🦜 4", "output": "6"},
    {"input": "What did the cow say to the moon?", "output": "nothing at all"},
    {
        "input": "Write me a poem about the moon",
        "output": "One for the moon, and one for me, who are we to talk about the moon?",
    },
]

to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Define the few-shot prompt.
few_shot_prompt = FewShotChatMessagePromptTemplate(
    # The input variables select the values to pass to the example_selector
    input_variables=["input"],
    example_selector=example_selector,
    # Define how each example will be formatted.
    # In this case, each example will become 2 messages:
    # 1 human, and 1 AI
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

print(few_shot_prompt.invoke(input="What's 3 🦜 3?"))
```