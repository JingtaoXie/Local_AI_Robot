from langchain_ollama import ChatOllama ##langchain ollama package



llm = ChatOllama(
    model="phi3",
    temperature=0,
)

messages = [
    ("system", "You are a Chinese AI. Answer all questions in Chinese."),
    ("human", "Hello, how are you?"),
]

ai_msg = llm.invoke(messages)

#模型invoke返回的信息包含很多参数，其中content里的才为回答本身
print(ai_msg.content)
