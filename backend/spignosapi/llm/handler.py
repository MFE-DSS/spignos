import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

class LLMHandler:
    def __init__(self):
        # 📁 Déduction du chemin local vers le dossier contenant le modèle
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.abspath(os.path.join(base_dir, '..', 'llm_models', 'mistral'))

        print(f"🔧 Chargement du modèle local depuis {self.model_path}...")

        # ✅ Chargement strictement local
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            local_files_only=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

        # Optionnel : Génération par défaut configurable
        self.generation_config = GenerationConfig.from_pretrained(
            self.model_path, local_files_only=True
        )

        print("✅ Modèle chargé localement avec succès.")

    def generate(self, prompt, max_tokens=256, temperature=0.7, top_p=0.95):
        # 🔢 Préparer les inputs
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # 🎯 Génération du texte
        outputs = self.model.generate(
            **inputs,
            generation_config=self.generation_config,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )

        # 🔽 Extraction de la réponse
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):].strip()
