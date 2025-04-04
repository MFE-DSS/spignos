import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLMHandler:
    def __init__(self):
        # 🔁 Chemin relatif vers le modèle stocké localement
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, '..', 'llm_models', 'mistral')

        # 🧠 Chargement du tokenizer et du modèle (une seule fois)
        print(f"🔧 Chargement du modèle depuis {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"  # auto = GPU si dispo
        )
        print("✅ Modèle chargé.")

    def generate(self, prompt, max_tokens=256, temperature=0.7, top_p=0.95):
        # 🔢 Préparation de l'entrée
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # 🎯 Génération
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )

        # 🧾 Extraction de la réponse
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):].strip()
