# Coach Udemy Agent – propose des formations adaptées en se basant sur l'analyse de Coach IT.
from prompts import mock_udemy_data


class CoachUdemy:
    """Agent proposant une ou plusieurs formations Udemy en se basant sur la recommandation de CoachIT."""

    def recommend_courses(self, analysis_text: str) -> str:
        """Détermine des formations à recommander à partir de l'analyse de Coach IT."""
        text_lower = analysis_text.lower()
        category = None
        # Identification simple de la filière recommandée dans l'analyse (selon mots-clés)
        if "développeur" in text_lower or "développement" in text_lower:
            category = "développeur web"
        elif "data" in text_lower or "données" in text_lower:
            category = "data science"
        elif "cyber" in text_lower or "sécurité" in text_lower:
            category = "cybersécurité"

        # Récupération des cours correspondant à la catégorie identifiée
        if category and category in mock_udemy_data.courses_by_field:
            courses = mock_udemy_data.courses_by_field[category]
            # Construire la liste de recommandations de cours
            recommandations = [f"- {c['title']} ({c['url']})" for c in courses]
            courses_text = "\n".join(recommandations)
            recommendation_text = (
                f"La recommandation de CoachIT est orientée vers **{category}**.\n"
                f"Voici quelques formations Udemy suggérées pour vous lancer :\n{courses_text}"
            )
        else:
            # Si aucune catégorie n'a été déduite de l'analyse
            recommendation_text = (
                "Sur la base de l'analyse du CoachIT, aucune spécialisation précise n'a été détectée pour proposer des formations ciblées. "
                "Vous pouvez explorer les formations Udemy populaires dans divers domaines de l'informatique pour affiner votre projet."
            )
        return recommendation_text
