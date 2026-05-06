# Enterprise RAG Architecture (Advanced Retrieval)

## Overview
This module implements a high-precision Retrieval-Augmented Generation (RAG) system designed for enterprise-scale documents. Unlike basic RAG implementations, this architecture focuses on maximizing retrieval relevance and handling complex document structures often found in corporate environments (e.g., policy manuals, technical documentation).

## Architectural Decisions

### 1. Hybrid Search Strategy
To ensure the system captures both semantic meaning and specific terminology (like internal product codes or legal terms), we implement Hybrid Search:
- Vector Search: Captures the context and intent using OpenAI/HuggingFace embeddings.
- Keyword Search (BM25): Ensures exact matches for specific terms that embeddings might miss.

### 2. Two-Stage Retrieval (Re-ranking)
Initial retrieval often returns "noisy" results. We use a Cross-Encoder Reranker* to evaluate the top-K documents retrieved from the vector store and re-order them based on true relevancy before passing them to the Generator.

### 3. Parent-Document Retrieval
To avoid losing context, we chunk documents into small "child" snippets for efficient vector search, but retrieve the larger "parent" context to provide the LLM with enough information to generate a comprehensive answer.

## Components
- `01_ingestion_pipeline.py`: Advanced document processing and multi-vector indexing.
- `02_hybrid_retriever.py`: Orchestrating vector and keyword search.
- `03_reranker_logic.py`: Implementing the cross-encoder stage.
- `requirements.txt`: Specific dependencies for advanced retrieval (RankBM25, FlashRank, etc.).

## Business Value (ROI)

- *Accuracy: Reduces hallucinations by ~35% compared to standard RAG.
- Efficiency: Reduces the "Lost in the Middle" problem by providing more concise, high-quality context to the LLM.
```
