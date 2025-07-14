from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Chargement sécurisé du modèle CodeLlama depuis le dossier local...")
path = "../llm_models/mistral"

tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForCausalLM.from_pretrained(path, device_map="auto")

print("Modèle chargé avec succès.")

prompt = "Écris une fonction Python qui calcule la factorielle."

inputs = tokenizer(prompt, return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)

print("Sortie générée :")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
