# langgraph overview

- [langgraph overview](#langgraph-overview)
  - [what is langgraph?](#what-is-langgraph)
    - [key features](#key-features)
  - [how to build langgraph](#how-to-build-langgraph)


## what is langgraph?

langgraph 是一个使用 LLM 来构建有状态，多角色应用的库，可用于创建 agent 以及多个 agent 协作的工作流；

### key features

```mermaid
flowchart LR
    s0[fa:fa-list-ul 关键特性]
    s1["fa:fa-step-forward 循环和分支: 能够实现循环和条件判断"]
    s2["fa:fa-step-forward 持久化: 执行图中步骤之后能够自动存储状态。<br/> 能够在随时暂停和恢复图的执行，<br/> 以达到错误恢复，人工干预，时间旅行等功能"]
    s3["fa:fa-step-forward 循环中的人类参与: <br/> 中断 agent 计划好的下一步，以便人类可以授权或编辑"]
    s4["fa:fa-step-forward 支持流式输出"]
    s5["fa:fa-step-forward 与 langchain 集成: 可集成 langchain 和 langsmith，但并不依赖"]

    s0 --> s1
    s0 --> s2
    s0 --> s3
    s0 --> s4
    s0 --> s5
```

## how to build langgraph

```mermaid
flowchart TB
    subgraph s1["fa:fa-step-forward 初始化 LLM 和工具"]
        direction LR
        s101["
#35; get llm
llm_model = llm.LLM(yml_config).get_llm()
#35; 定义一个工具列表，初始包含一个名为search的工具
tools = [search]
#35; 绑定工具节点到LLM模型，使得模型可以调用工具节点中的工具
model = llm_model.bind_tools(tools=tools)
        "]
    end

    subgraph s2["fa:fa-step-forward 初始化带状态的 graph"]
        s201["
#35; 创建一个工作流，用于处理对话
workflow = StateGraph(MessagesState)
        "]
    end

    subgraph s3["fa:fa-step-forward 定义图的节点"]
        s301["
#35; 添加图的节点
workflow.add_node('agent', call_model)
workflow.add_node('tools', tool_node)        
        "]
    end

    subgraph s4["fa:fa-step-forward 定义图的入口点及边"]
        s401["
#35; 添加图的边及条件边
workflow.add_edge(START, 'agent')
workflow.add_conditional_edges('agent', should_continue)
workflow.add_edge('tools', 'agent')        
        "]
    end

    subgraph s5["fa:fa-step-forward 编译图"]
        s501["
#35; 创建一个检查点，用于保存对话状态
checkpointer = MemorySaver()

#35;  编译工作流，生成一个可执行的应用程序
app = workflow.compile(checkpointer=checkpointer)        
        "]
    end

    subgraph s6["fa:fa-step-forward 执行图"]
        s601["
config = {'configurable': {'thread_id': 111}}
final_state = app.invoke(
    {'messages': [HumanMessage(content='what's the weather like in san francisco?')]},
    config=config,
)

print(final_state['messages'][-1].content)        
        "]
    end


    s1 --> s2 --> s3 --> s4 --> s5 --> s6
```

完整代码详见: [langgraph_example.py](https://github.com/ka1fe1/tutorial-langchain/tree/main/tutorial-app/langgraph/0-overview/example.py)

