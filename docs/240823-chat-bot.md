# 240823-聊天机器人
- [240823-聊天机器人](#240823-聊天机器人)
  - [Message History](#message-history)
  - [Managing Chat History](#managing-chat-history)

## Message History

聊天机器人的关键在于管理对话历史，在 langchain 中，可以通过 `RunnableWithMessageHistory` 来实现。

RunnableWithMessageHistory 是 LangChain 中用于管理对话历史的关键类。它允许在多个会话中有效地管理对话历史，提供连贯和上下文相关的响应。以下是 RunnableWithMessageHistory 的主要参数及其作用：

1. `chain`: 要运行的链或可运行对象。这是处理输入并生成输出的核心组件。
2. `get_session_history`: 函数，接收 session_id 并返回 BaseChatMessageHistory 对象。用于存储和检索特定会话的消息历史。
3. `input_messages_key`: 字符串，指定输入字典中包含消息的键名。告诉 RunnableWithMessageHistory 在哪里找到新的输入消息。
4. `history_messages_key`: 可选，字符串，指定输出字典中存储历史消息的键名。如果不指定，历史消息将直接添加到输入消息中。
5. `output_messages_key`: 可选，字符串，指定输出字典中存储新生成消息的键名。如果不指定，新消息将直接添加到历史消息中。

> 
> code: [RunnableWithMessageHistory](https://github.com/ka1fe1/tutorial-langchain/blob/main/tutorial-app/2_chat_bot.py#L67)

## Managing Chat History

管理对话历史的关键在于使用 trim_messages 来修剪消息历史，以保持对话的清晰和相关性。

trim_messages 对象有以下参数及其作用:

- `max_tokens`: 设置消息历史的最大令牌数。这有助于控制历史的长度，防止它变得过长。
- `strategy`: 定义如何修剪消息。常用的策略包括：
  - "last": 保留最近的消息，删除较早的消息。
  - "first": 保留最早的消息，删除较新的消息。
- `token_counter`: 用于计算消息中的令牌数的函数或对象。通常使用语言模型来执行此操作。
- `include_system`: 布尔值，决定是否在修剪过程中包含系统消息。
- `allow_partial`: 布尔值，决定是否允许部分消息被保留。如果设为 False，将只保留完整的消息。
- `start_on`: 指定从哪种类型的消息开始保留。例如，"human" 表示从人类消息开始保留。

这些参数允许灵活地控制如何修剪和管理对话历史，以确保保留最相关的信息，同时保持历史的简洁性和效率。

> code: [ManagingConversationHistory](https://github.com/ka1fe1/tutorial-langchain/blob/main/tutorial-app/2_chat_bot.py#L124)
