# example selectors

示例选择器的作用是选择正确的少量示例给到提示词

## custom example selector

1. 继承 `BaseExampleSelector`，并实现 `select_examples` 抽象方法

## example selector type

| name | desc |
| --- | --- |
| Similarity | Uses semantic similarity between inputs and examples to decide which examples to choose. |
| MMR | Uses Max Marginal Relevance between inputs and examples to decide which examples to choose. |
| Length | Selects examples based on how many can fit within a certain length |
| Ngram | Uses ngram overlap between inputs and examples to decide which examples to choose. |

直接使用 langchain 内置类即可，详见: [https://python.langchain.com/docs/how_to/#example-selectors](https://python.langchain.com/docs/how_to/#example-selectors)