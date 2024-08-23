# 240823-聊天机器人

## Message History

聊天机器人的关键在于管理对话历史，在 langchain 中，可以通过 `RunnableWithMessageHistory` 来实现。

`RunnableWithMessageHistory` 需要三个参数:
- `chain`：要运行的链或可运行对象，它将处理输入并生成输出。
- `get_session_history`：一个函数，接收 session_id 并返回 BaseChatMessageHistory 对象，用于存储和检索特定会话的消息历史。
- `input_messages_key`：指定输入字典中包含消息的键名。这个参数告诉 RunnableWithMessageHistory 在哪里找到新的输入消息。

这三个参数的作用如下：
1. `chain` 定义了如何处理输入并生成响应。
2. `get_session_history` 允许为每个会话维护单独的对话历史，确保对话的连续性和上下文相关性。
3. `input_messages_key` 使系统能够正确识别和处理新的输入消息，将其与历史消息结合。

通过这种方式，`RunnableWithMessageHistory` 能够在多个会话中有效地管理对话历史，提供连贯和上下文相关的响应。

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
