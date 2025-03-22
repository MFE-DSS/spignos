import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LLM_MODEL_PATH = os.path.join(BASE_DIR, '../../llm_models/mistral')  # Adapté pour être relatif à settings.py

class LLMHandler:
    def __init__(self):
        print("[INFO] Loading local LLM model from:", LLM_MODEL_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_PATH)
        self.model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_PATH)
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_response(self, prompt, max_length=100):
        output = self.pipeline(prompt, max_new_tokens=max_length, do_sample=True, temperature=0.7)
        return output[0]["generated_text"]
