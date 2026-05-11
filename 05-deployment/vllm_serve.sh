```bash
#!/bin/bash

# ==============================================================================
# TECHNICAL DECISION: vLLM for High-Throughput Serving
# ==============================================================================
# We use vLLM because of PagedAttention, which reduces memory waste and
# increases the serving capacity by up to 10x compared to vanilla transformers.
# ==============================================================================

python3 -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3-8B-Instruct \
    --quantization awq \
    --dtype half \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.9 \
    --port 8000