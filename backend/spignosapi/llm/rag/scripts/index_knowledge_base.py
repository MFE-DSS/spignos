import os

import docx  # Pour lire DOCX
import fitz  # PyMuPDF pour lire PDF

from ..embedding import EmbeddingModel
from ..faiss_index import FaissIndex

# 🔹 Chemin vers knowledge_base
BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")

# 🔹 Initialisation des modèles embedding et index FAISS
embedding_model = EmbeddingModel()
faiss_index = FaissIndex()


# 🔹 Fonction d'extraction du texte pour PDF
def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# 🔹 Fonction d'extraction du texte pour DOCX
def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])


"""
# 🔹 Indexation automatique des fichiers
def index_documents(base_path):
    documents = []
    embeddings = []

    # Parcourt chaque sous-dossier et fichier
    for root, dirs, files in os.walk(base_path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if file.endswith(".pdf"):
                    text = extract_text_from_pdf(filepath)
                elif file.endswith(".docx"):
                    text = extract_text_from_docx(filepath)
                else:
                    continue  # ignore autres formats

                # Diviser le texte en petits chunks pour mieux indexer
                chunks = split_text_into_chunks(text)
                documents.extend(chunks)

            except Exception as e:
                print(f"Erreur avec {file}: {e}")

    # Générer embeddings pour tous les documents/chunks extraits
    embeddings = [embedding_model.embed_text(chunk) for chunk in documents]

    # Ajouter à FAISS
    faiss_index.add_documents(embeddings, documents)
    print(f"{len(documents)} documents/chunks indexés avec succès.")


# 🔹 Découpe simple des textes longs en chunks (max 500 caractères)
def split_text_into_chunks(text, chunk_size=500):
    paragraphs = text.split("\n")
    chunks, current_chunk = [], ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    index_documents(BASE_PATH)
"""
