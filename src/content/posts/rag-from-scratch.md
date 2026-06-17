---
title: "RAG 架构实战：从零搭建一个文档问答系统"
date: 2026-06-01T10:00:00+08:00
categories: ["AI"]
description: "用 LangChain + Chroma + OpenAI 搭建 RAG 系统的完整步骤，附带性能优化技巧"
---

RAG（Retrieval-Augmented Generation）是让 LLM 回答私有文档的核心方案。

## 架构概览

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ 文档切分  │ → │ 向量嵌入  │ → │ 向量存储  │
└──────────┘    └──────────┘    └──────────┘
                                      │
┌──────────┐    ┌──────────┐          │
│ LLM 生成  │ ← │ 检索召回  │ ←────────┘
└──────────┘    └──────────┘
```

## 核心代码

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 1. 文档切分
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 2. 向量化 + 存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. 检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
docs = retriever.get_relevant_documents("Doris 3.0 新特性")

# 4. 生成
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
answer = qa.run("Doris 3.0 有哪些新特性？")
```

## 关键优化

- **Chunk size**：500-1000 token 最佳。太短缺上下文，太长噪音多
- **Overlap**：chunk_size 的 10%，保证信息不丢失
- **Embedding 模型**：text-embedding-3-small 性价比最高
- **检索策略**：MMR（最大边际相关性）避免重复文档

> RAG 的本质是把「LLM 不知道的东西」提前塞进 prompt。
