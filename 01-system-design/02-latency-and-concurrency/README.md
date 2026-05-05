# Latency and Concurrency Management

## Overview
In high-traffic Enterprise AI applications (such as banking or fintech systems), managing API costs, reducing response latency, and handling high concurrent requests are critical challenges. This module demonstrates two key architectural patterns used to optimize performance: **Semantic Routing** and **Semantic Caching**.

## Concepts Covered

### 1. Semantic Router (`01_semantic_router.py`)
Sending every user query to a heavy, expensive LLM (like GPT-4) is inefficient. 
- **The Pattern**: We use a lightweight embedding model to classify the "intent" of the query before it reaches the main LLM.
- **Benefits**: 
    - Redirects queries to specialized models (e.g., a finance-tuned model for banking queries vs. a generic model for small talk).
    - Prevents "Prompt Injection" or "Out-of-Scope" queries from reaching expensive resources.

### 2. Semantic Caching (`02_semantic_cache.py`)
Traditional exact-match caching (like Redis) fails in LLM applications because users rarely ask the exact same question twice.
- **The Pattern**: We store previous query-response pairs in a Vector Database (FAISS). When a new query arrives, we check if a *semantically similar* question has been answered before.
- **Benefits**:
    - **Zero Latency**: Answers are returned instantly from the local database.
    - **Cost Reduction**: Eliminates the need for API calls to OpenAI/Anthropic for redundant questions.

## Implementation Details

### Prerequisites
Install dependencies using the local requirements file:
```bash
pip install -r requirements.txt

### How to Run
1.  *Set up Environment: Ensure your `.env` file contains your `OPENAI_API_KEY`.
2.  Run Router: 
    python 01_semantic_router.py
    
3.  Run Cache:
    python 02_semantic_cache.py
    

## Performance Impact
By combining these two patterns, an enterprise system can typically:
- Reduce LLM API costs by 30-50% via Caching.
- Improve system throughput by routing simple tasks to smaller, faster models.
```