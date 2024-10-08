# How to return structured data from a model

## Why need it?

最常用的用途就是从 LLM 中提取数据并插入到 `db` 中或者给到下游的系统使用

## How return structured data from a model?

有以下两种方式

### With `with_structured_output` method

基本语法如下:
```python
    llm.with_structured_output()
```


### Prompting and parsing model output directly

在提示词中使用特定的格式，并使用输出解析器来提取结构化数据

有以下 2 种方式来实现:

1. 使用 `PydanticOutputParser` 模型
2. 使用 custom parsing

