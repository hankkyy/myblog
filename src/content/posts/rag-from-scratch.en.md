---
lang: en
title: "RAG Architecture in Practice: Building a Document Q&A System from Scratch"
date: 2026-06-01T10:00:00+08:00
categories: ["AI"]
description: "Complete steps to build a RAG system using LangChain + Chroma + OpenAI, with performance optimization tips"
---

RAG (Retrieval-Augmented Generation) is the core solution for enabling LLMs to answer questions about private documents.

## Architecture Overview

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Chunking │ → │ Embedding │ → │ Vector DB │
└──────────┘    └──────────┘    └──────────┘
                                      │
┌──────────┐    ┌──────────┐          │
│ LLM Gen  │ ← │ Retrieval │ ←────────┘
└──────────┘    └──────────┘
```

## Core Code

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 1. Document chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 2. Embedding + storage
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. Retrieval
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
docs = retriever.get_relevant_documents("Doris 3.0 new features")

# 4. Generation
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
answer = qa.run("What are the new features in Doris 3.0?")
```

## Key Optimizations

- **Chunk size**: 500-1000 tokens is optimal. Too small loses context, too large introduces noise
- **Overlap**: 10% of chunk_size to ensure no information is lost
- **Embedding model**: text-embedding-3-small offers the best cost-performance ratio
- **Retrieval strategy**: MMR (Maximum Marginal Relevance) avoids duplicate documents

> The essence of RAG is to inject "what the LLM doesn't know" into the prompt in advance.

---

**References:**

- [Lewis et al. — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](https://arxiv.org/abs/2005.11401)