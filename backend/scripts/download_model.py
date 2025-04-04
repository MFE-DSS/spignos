import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Nom du modèle Hugging Face
model_name = "codellama/CodeLlama-7b-Python-hf"

# Répertoire local où enregistrer le modèle
local_model_path = os.path.join("..", "llm_models", "mistral")

# Vérifie si le modèle existe déjà localement
if not os.path.exists(local_model_path):
    print(f"Téléchargement du modèle {model_name} vers {local_model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Sauvegarde locale
    tokenizer.save_pretrained(local_model_path)
    model.save_pretrained(local_model_path)
    print("Téléchargement et sauvegarde terminés.")
else:
    print(f"Le modèle est déjà présent dans {local_model_path}.")
