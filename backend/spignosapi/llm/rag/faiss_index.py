# spignosapi/llm/rag/faiss_index.py

import os
import pickle

import faiss
import numpy as np


class FaissIndex:
    """
    Gestion complète de l'index vectoriel FAISS :
    - Indexation des embeddings des documents métiers.
    - Recherche contextuelle pour enrichir les prompts.
    - Persistance sur disque.
    """

    def __init__(self, index_path=None, meta_path=None, embedding_dim=384):
        """
        Initialise l'index FAISS et charge les données existantes (si présentes).

        Args:
            index_path (str): Chemin vers le fichier d'index FAISS.
            meta_path (str): Chemin vers les métadonnées associées.
            embedding_dim (int): Dimension des embeddings (384 pour 'all-MiniLM-L6-v2').
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_path = index_path or os.path.join(base_dir, "faiss_index.index")
        self.meta_path = meta_path or os.path.join(base_dir, "metadata.pkl")

        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata = []

        self._load_or_initialize()

    def _load_or_initialize(self):
        """
        Charge l'index et les métadonnées si présents, sinon initialise un nouvel index.
        """
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            print("✅ FAISS Index chargé avec succès.")
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.metadata = []
            print("⚠️ Nouvel index FAISS initialisé.")

    def add_documents(self, embeddings, docs_metadata):
        """
        Ajoute des documents et leurs embeddings dans l'index FAISS.

        Args:
            embeddings (np.ndarray): Embeddings des documents à indexer.
            docs_metadata (list[str]): Textes ou métadonnées des documents à stocker.
        """
        if len(embeddings) != len(docs_metadata):
            raise ValueError("La longueur des embeddings et des métadonnées doit être identique.")

        self.index.add(np.array(embeddings).astype(np.float32))
        self.metadata.extend(docs_metadata)
        self._save_index()

    def retrieve_contexts(self, query_embedding, k=3):
        """
        Recherche les contextes les plus pertinents à partir d'un embedding utilisateur.

        Args:
            query_embedding (np.ndarray): Embedding du texte utilisateur.
            k (int): Nombre de résultats contextuels à retourner.

        Returns:
            list[str]: Textes des documents les plus pertinents.
        """
        if self.index.ntotal == 0:
            print("⚠️ L'index FAISS est vide. Aucun contexte trouvé.")
            return []

        query_vector = np.array([query_embedding]).astype(np.float32)
        distances, indices = self.index.search(query_vector, k)

        contexts = [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        return contexts

    def _save_index(self):
        """
        Sauvegarde l'index FAISS et les métadonnées sur disque.
        """
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print("✅ FAISS Index et métadonnées sauvegardés avec succès.")
