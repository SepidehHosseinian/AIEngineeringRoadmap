# ⚡ Model Serving Strategies

When deploying models, we choose the serving strategy based on the Latency vs. Throughput trade-off.

### 1. Synchronous API (FastAPI/Flask)
- Best for: Small models, low traffic, or internal tools.
- Pros: Simple to implement.
- Cons: Blocks the thread during heavy inference; not suitable for LLMs.

### 2. Async Task Queue (Celery + Redis)
- Best for: Long-running tasks (e.g., Credit Scoring reports, PDF OCR).
- Pros: User doesn't wait for the result; highly scalable.
- Cons: Requires a more complex architecture.

### 3. Specialized Inference Servers (vLLM / Triton)
- Best for: High-traffic LLMs or Multi-modal models.
- Pros: Uses Continuous Batching to handle multiple requests at once, saving up to 80% on GPU costs.
- Cons: Higher initial setup complexity.

### 🧭 My Recommendation for Production:
For a banking environment, I recommend a Hybrid Approach: Use vLLM for the core LLM inference and an Asynchronous Queue for document processing jobs to ensure the system remains responsive under heavy load.
