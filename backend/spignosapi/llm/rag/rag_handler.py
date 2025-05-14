# spignosapi/llm/rag/rag_handler.py

from .embedding import EmbeddingModel
from .faiss_index import FaissIndex
from ..handler import UnifiedLLMHandler


class RAGHandler:
    def __init__(self, use_openai=True):
        # Initialisation des dépendances
        self.embedding_model = EmbeddingModel()
        self.faiss_index = FaissIndex()
        self.llm_handler = UnifiedLLMHandler(use_openai=use_openai)

    def enrich_and_generate(self, user_input, k=3, max_tokens=512, temperature=0.7):
        """
        Génère une réponse enrichie par RAG.

        Étapes :
        1. Embedding de la requête utilisateur
        2. Recherche contextuelle via FAISS
        3. Assemblage d'un prompt enrichi
        4. Génération via LLM (OpenAI ou local)
        """

        # Génération de l'embedding utilisateur
        user_embedding = self.embedding_model.embed_text(user_input)

        # Récupération des contextes pertinents avec FAISS
        contexts = self.faiss_index.retrieve_contexts(user_embedding, k=k)

        # Construction du prompt enrichi
        enriched_prompt = self._build_prompt(user_input, contexts)

        # Génération de la réponse via le LLM
        response = self.llm_handler.generate(enriched_prompt)

        return response

    @staticmethod
    def _build_prompt(user_input, contexts):
        """
        Assemblage précis du prompt final, prêt à être envoyé au LLM.
        """
        context_text = "\n---\n".join(contexts)

        return (
            "Tu es un assistant expert en documentation technique pour projets informatiques.\n"
            "Voici des extraits de documents techniques pertinents pour t’aider à répondre :\n\n"
            f"{context_text}\n\n"
            "Demande utilisateur :\n"
            f"{user_input}\n\n"
            "Document technique généré :"
        )
