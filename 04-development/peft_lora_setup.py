"""
================================================================================
TECHNICAL DECISION: Parameter-Efficient Fine-Tuning (PEFT) using LoRA
================================================================================

1. CONTEXT:
   Fine-tuning an entire 70B model is computationally prohibitive. 
   LoRA (Low-Rank Adaptation) allows us to tune only a tiny fraction (<1%) 
   of parameters.

2. WHEN TO USE THIS OVER RAG:
   - To inject a specific "Tone of Voice" or "Style".
   - To master a complex structured output (e.g., specialized JSON).
   - To learn domain-specific jargon that a base model doesn't understand.

3. BUSINESS VALUE:
   - Lower GPU Requirements: Can be done on consumer-grade or mid-tier GPUs.
   - Faster Iteration: Training takes hours, not days.
================================================================================
"""

from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

def prepare_lora_model(model_name: str):
    # 1. Load Base Model (using 4-bit quantization for efficiency)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        load_in_4bit=True
    )
    
    # 2. Define LoRA Configuration
    # We only target the attention layers (q_proj, v_proj)
    config = LoraConfig(
        r=16, # Rank: higher means more parameters but more capacity
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # 3. Apply LoRA to the model
    peft_model = get_peft_model(model, config)
    
    # Print trainable parameters to show efficiency
    peft_model.print_trainable_parameters()
    
    return peft_model

if __name__ == "__main__":
    MODEL_ID = "meta-llama/Meta-Llama-3-8B"
    # In a real scenario, we would run this. Here it's for architectural demo.
    print(f"🛠️ Initializing LoRA adapter for {MODEL_ID}...")
    # model = prepare_lora_model(MODEL_ID)