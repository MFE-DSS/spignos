# spignosapi/llm/rag/embedding.py

from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    """
    Modèle de génération d'embeddings basé sur SentenceTransformer,
    compatible directement avec rag_handler.py et faiss_index.py.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialise et charge le modèle SentenceTransformer.

        Args:
            model_name (str): Nom du modèle d'embedding SentenceTransformer.
                              'all-MiniLM-L6-v2' est performant et rapide.
        """
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text):
        """
        Génère l'embedding vectoriel d'un texte donné.

        Args:
            text (str): Le texte à transformer en embedding.

        Returns:
            np.ndarray: Embedding sous forme de vecteur numpy.
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)
