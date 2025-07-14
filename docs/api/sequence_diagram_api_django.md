
Utilisateur -> API SPIGNOS : POST /api/conversations/{id}/messages

API SPIGNOS -> Système : Valider les données du message

Système -> Base de données : Enregistrer le message

Base de données -> Système : Confirmation d'enregistrement

Système -> API SPIGNOS : Réponse avec le message créé

API SPIGNOS -> Utilisateur : Réponse HTTP 201 avec les détails du message
