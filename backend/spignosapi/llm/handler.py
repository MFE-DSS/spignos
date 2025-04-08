import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMHandler:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "llm_models", "mistral")
        )

    def _load_model(self):
        if self.model is None or self.tokenizer is None:
            print(f"🚀 Chargement du modèle LLM depuis {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto",
                local_files_only=True
            )
            print("✅ Modèle chargé en mémoire.")

    def generate(self, prompt, max_tokens=256, temperature=0.7, top_p=0.95):
        self._load_model()

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)[len(prompt):].strip()
