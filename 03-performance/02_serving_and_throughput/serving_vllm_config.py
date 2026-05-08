"""
================================================================================
TECHNICAL DECISION: High-Throughput Serving with vLLM & PagedAttention
================================================================================

1. CONTEXT:
   Standard inference (HuggingFace) handles requests one by one or in static 
   batches, leading to GPU underutilization (60-70% idle time). For a 
   high-traffic app, we need to maximize Throughput.

2. PROBLEM SOLVED:
   - KV-Cache Fragmentation: PagedAttention manages memory like an OS, 
     eliminating 96% of memory waste.
   - Wait Times: Continuous Batching allows new requests to join the batch 
     immediately without waiting for the previous ones to finish.

3. BUSINESS VALUE:
   - Scalability: Handles 10x-20x more concurrent users on the same hardware.
   - Cost: Reduces the number of GPUs needed in the cluster.

4. IMPLEMENTATION:
   - vLLM Engine initialization.
   - Tensor Parallelism (TP) for multi-GPU distribution.
================================================================================
"""

from vllm import LLM, SamplingParams

class VLLMInferenceEngine:
    def init__(self, model_id: str, gpu_count: int = 1):
        """
        Initializes the vLLM engine with PagedAttention and TP.

        Args:
            gpu_count: Number of GPUs to use (Tensor Parallelism). 
                       Crucial for models like Llama-3-70B.
        """
        self.model_id = model_id

        print(f"🚀 Initializing vLLM Engine with {gpu_count} GPU(s)...")

        # TECHNICAL DETAIL: tensor_parallel_size is the key for Multi-GPU
        self.llm = LLM(
            model=model_id,
            tensor_parallel_size=gpu_count,
            trust_remote_code=True,
            gpu_memory_utilization=0.90, # Leave 10% for system/overhead
            max_model_len=4096 # Managed by PagedAttention efficiently
        )

    def generate_batch(self, prompts: list[str]):
        """
        Demonstrates Continuous Batching. 
        Requests are processed dynamically.
        """
        # Setting sampling parameters (Max tokens, Temperature, etc.)
        sampling_params = SamplingParams(
            temperature=0.8,
            top_p=0.95,
            max_tokens=256,
            presence_penalty=1.1 # Prevent repetitive outputs
        )

        print(f"⚙️ Processing a batch of {len(prompts)} requests concurrently...")

        outputs = self.llm.generate(prompts, sampling_params)

        results = []
        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            results.append({"prompt": prompt, "answer": generated_text})

        return results

# --- Production Scenario Simulation ---

if __name == "__main__":
    # In a real Lead role, you'd be deciding between:
    # 1. Tensor Parallelism (TP): Splitting layers ACROSS GPUs (Faster for single request)
    # 2. Pipeline Parallelism (PP): Splitting layers IN SEQUENCE (Better for throughput)

    MODEL_NAME = "meta-llama/Meta-Llama-3-8B"


    # Simulating a multi-GPU setup (e.g., 2x A100 or 2x RTX 3090)
    engine = VLLMInferenceEngine(model_id=MODEL_NAME, gpu_count=1)

    user_requests = [
        "What is the interest rate for a loan?",
        "How do I activate my AzkiVam card?",
        "Explain the credit scoring process in simple terms.",
        "Why was my application rejected?"
    ]

    # This doesn't run sequentially; vLLM's scheduler batches them perfectly.
    responses = engine.generate_batch(user_requests)

    for i, res in enumerate(responses):
        print(f"\nUser {i+1}: {res['prompt']}")
        print(f"AI: {res['answer'][:50]}...")