from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Chemin vers ton modèle local
local_path = "../llm_models/mistral"

# Chargement du tokenizer et du modèle
tokenizer = AutoTokenizer.from_pretrained(local_path)
model = AutoModelForCausalLM.from_pretrained(local_path)

# Passage en évaluation
model.eval()

# Prompt de test
prompt = "Écris une fonction Python qui trie une liste."

inputs = tokenizer(prompt, return_tensors="pt")

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
