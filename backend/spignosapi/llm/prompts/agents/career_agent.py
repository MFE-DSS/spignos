# Coach IT Agent – fournit une analyse personnalisée de reconversion IT.
# On suppose que UnifiedLLMHandler est une classe utilitaire existante pour interroger l'API OpenAI.
from myproject.llm_handler import UnifiedLLMHandler  # Adapter l'import en fonction du projet


class CoachIT:
    """Agent fournissant une analyse personnalisée pour un projet de reconversion IT."""

    def __init__(self, llm_handler=None):
        # Si aucun handler n'est fourni, on en crée un par défaut (configuré pour OpenAI)
        self.llm_handler = llm_handler if llm_handler is not None else UnifiedLLMHandler()
        # Prompt système définissant le rôle de Coach IT
        self.system_prompt = (
            "Vous êtes CoachIT, un expert en reconversion professionnelle dans le domaine de l'informatique. "
            "Votre rôle est de fournir une analyse personnalisée et détaillée du projet de reconversion de l'utilisateur vers une carrière IT. "
            "Répondez de manière structurée, pédagogique et en français."
        )

    def analyze_project(self, user_input: str) -> str:
        """Interroge l'LLM pour obtenir l'analyse du projet de reconversion."""
        # Préparation des messages pour l'API OpenAI (conversationnelle)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]
        # Appel du modèle via le handler unifié
        analysis_text = self.llm_handler.ask(messages)
        return analysis_text
