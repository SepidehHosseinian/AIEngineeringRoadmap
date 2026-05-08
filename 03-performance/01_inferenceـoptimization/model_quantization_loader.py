"""
================================================================================
TECHNICAL DECISION: Model Quantization (4-bit/8-bit)
================================================================================

1. CONTEXT:
   Large Language Models (like Llama-3 70B) require massive VRAM (140GB+). 
   In enterprise environments like Behsazan, we often need to run models on 
   limited hardware while maintaining private data on-premise.

2. PROBLEM SOLVED:
   - Hardware Barriers: Reduces VRAM usage by 4x to 8x. A model that needed 
     40GB GPU can now run on a 10GB or 12GB consumer-grade GPU.
   - Cost: Lower GPU requirements mean lower cloud/infrastructure costs.

3. BUSINESS VALUE:
   - Privacy-First AI: Enables running powerful models on local servers instead 
     of sending data to OpenAI/external APIs.
   - Faster Deployment: Smaller model files are quicker to load and transfer.

4. TECHNICAL IMPLEMENTATION:
   - Uses BitsAndBytes for 4-bit NormalFloat (NF4) quantization.
   - Implements "Double Quantization" to save additional memory.
================================================================================
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

class QuantizedModelLoader:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

    def load_4bit_model(self):
        """
        Loads a model in 4-bit precision using bitsandbytes.
        This is the industry standard for running LLMs on limited VRAM.
        """
        print(f"🚀 Loading model {self.model_id} in 4-bit...")

        # Configuration for 4-bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4", # Normal Float 4: better than linear for weights
            bnb_4bit_use_double_quant=True, # Quantize the quantization constants
            bnb_4bit_compute_dtype=torch.bfloat16 # Computation happens in BF16 for speed
        )

        try:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                quantization_config=bnb_config,
                device_map="auto", # Automatically balance across available GPUs
                trust_remote_code=True
            )
            print("✅ Model loaded successfully with 4-bit quantization.")
            return model
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None

    def get_model_memory_footprint(self, model):
        """Calculates how much VRAM the model is actually using."""
        if model:
            mem = model.get_memory_footprint() / (1024*3) # Convert to GB
            print(f"📊 Model Memory Footprint: {mem:.2f} GB")
            return mem

# --- Usage Example for a Lead/Architect ---
if name == "__main__":
    # Example using a popular small model (Mistral or Llama)
    MODEL_NAME = "mistralai/Mistral-7B-v0.1"

    loader = QuantizedModelLoader(MODEL_NAME)


    # Note: Running this requires a GPU with bitsandbytes installed
    # In an interview, you explain that this reduces a 14GB model to ~4-5GB.
    print("Scenario: Deploying Mistral-7B on a single T4 or RTX 3060 GPU.")

    # model = loader.load_4bit_model()
    # loader.get_model_memory_footprint(model)