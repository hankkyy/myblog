---
lang: en
title: "Docker Image Layer Caching: Why COPY Order Affects Build Speed"
date: 2025-01-18T10:00:00+08:00
categories: ['Technology']
description: "Understand how Docker layer caching works and best practices through a simple Spring Boot project."
---

Docker's image layer caching is a very important yet often overlooked concept.

## What Are Layers

Docker images are composed of multiple read-only layers stacked together. Each instruction in a Dockerfile (FROM, RUN, COPY, etc.) creates a new layer. These layers are cached—if a layer hasn't changed, Docker reuses the cache directly and skips rebuilding it.

## A Typical Example

```dockerfile
# Bad practice
COPY . /app
RUN mvn package

# Good practice
COPY pom.xml /app
RUN mvn dependency:resolve
COPY src /app/src
RUN mvn package
```

Why is the second approach faster? Because `pom.xml` changes far less frequently than source code. By downloading and caching dependencies first, you only need to recompile when code changes, without re-downloading dependencies every time.

## Key Principles

- Place operations with low change frequency first (installing system dependencies, downloading Maven/npm dependencies)
- Place operations with high change frequency later (COPY source code, compilation)
- Leverage multi-stage builds to reduce image size

Understanding layer caching can speed up Docker builds several times over.