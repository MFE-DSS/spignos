import os
from huggingface_hub import snapshot_download

# === CONFIGURATION ===
model_name = "codellama/CodeLlama-7b-Python-hf"
local_model_path = os.path.abspath(os.path.join("..", "llm_models", "mistral"))

# === TÉLÉCHARGEMENT SANS CHARGEMENT DU MODÈLE ===
print(f"📥 Téléchargement sans chargement en mémoire de {model_name}")
print(f"📁 Dossier local : {local_model_path}")

if not os.path.exists(local_model_path):
    os.makedirs(local_model_path, exist_ok=True)

# Télécharge les fichiers sans jamais instancier un modèle
snapshot_download(
    repo_id=model_name,
    local_dir=local_model_path,
    local_dir_use_symlinks=False,
    revision="main",
    resume_download=True,
)

print("✅ Modèle téléchargé avec succès.")
