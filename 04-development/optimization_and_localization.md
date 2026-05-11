# 🛠️ Model Optimization & Domain Adaptation Strategy

This document outlines the technical framework for making Large Language Models (LLMs) production-ready, focusing on efficiency and domain-specific accuracy.

---

## 1. Optimization Techniques (Production-Ready Models)

### A. Quantization (Size vs. Quality)
We use quantization to shrink models from 16-bit (FP16) to 4-bit or 8-bit, allowing them to run on cost-effective hardware.

| Technique | Format | Best Use Case |
| :--- | :--- | :--- |
| GGUF | Llama.cpp | CPU + GPU inference, great for local dev and edge. |
| AWQ | AutoAWQ | High-speed GPU inference (vLLM/TGI), best for production. |
| EXL2 | ExLlamaV2 | Extremely fast inference for specific NVIDIA architectures. |

Decision: For the current architecture, we prioritize AWQ for its balance of speed and performance in multi-user environments.

### B. Knowledge Distillation
To reduce latency, we implement a Teacher-Student framework:
- Teacher: A frontier model (e.g., Llama-3-70B) generates high-quality reasoning paths.
- Student: A smaller model (e.g., Llama-3-8B) is fine-tuned on these paths.
- Result: We achieve "70B logic" with "8B speed".

---

## 2. Multilingual & Domain-Specific Challenges

### A. The "Persian" Challenge (Tokenization)
Standard tokenizers often fragment Persian words into too many tokens (e.g., "سلام" might be 3-4 tokens). 
- Strategy: We evaluate models based on their Fertility Rate (tokens per word).
- Action: If needed, we perform Vocabulary Expansion by adding common Persian Fintech terms to the tokenizer and resizing the embedding layer.

### B. Domain-Specific SFT (Supervised Fine-Tuning)
In Fintech (like AzkiVam or similar), general models might confuse "Credit" with "Loan" or "Installment".
- SFT Dataset: We curate a dataset of 5,000+ instruction-response pairs focusing on:
    - Central Bank of Iran (CBI) regulations.
    - Sharia-compliant financial products.
    - Specific Iranian payment gateway error codes.