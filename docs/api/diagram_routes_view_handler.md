```plantuml
@startuml

skinparam packageStyle rectangle

package "Frontend Routes" {
    [Home (/chat/home/)] --> [Chat (/chat/)]
}

package "Authentication" {
    [Login (/accounts/login/)]
    [Logout (/accounts/logout/)]
}

package "REST API" {
    [ChatAPI POST /api/chat/]
    [ConversationMessagesAPI GET /api/chat/<conversation_id>/]
}

package "Views / Handlers" {
    [chat_page view]
    [home_page view]
    [ChatAPI DRF view]
    [ConversationMessagesAPI DRF view]
}

package "LLM Handlers" {
    [UnifiedLLMHandler]
    [OpenAIHandler]
    [LLMHandler (local)]
}

' Navigation frontend
[Home (/chat/home/)] --> [Login (/accounts/login/)]
[Login (/accounts/login/)] --> [Chat (/chat/)]

' Chat page POST triggers ChatAPI
[Chat (/chat/)] --> [ChatAPI POST /api/chat/]

' API flow
[ChatAPI POST /api/chat/] --> [UnifiedLLMHandler]
[UnifiedLLMHandler] --> [OpenAIHandler]
[UnifiedLLMHandler] --> [LLMHandler (local)]

' History view
[Chat (/chat/)] --> [ConversationMessagesAPI GET /api/chat/<conversation_id>/]

' Views mapping
[Chat (/chat/)] --> [chat_page view]
[Home (/chat/home/)] --> [home_page view]

@enduml



Ce diagramme décrit :
- Le **flux navigation frontend**.
- Le **flux API backend**.
- L'appel au **UnifiedLLMHandler** qui décide OpenAI ou local.
- La séparation claire Views / API / Handlers.

---

## 📝 2️⃣ Problème d’accès non sécurisé + page login non trouvée

**Actuellement :**
- La page `home` **ne redirige pas si l'utilisateur n'est pas authentifié** (ce qu'elle devrait faire).
- `/login/` renvoie une 404 car tu n’as pas encore défini `login.html` dans le bon dossier `templates/registration/login.html` **(Django attend ce chemin exact par convention)**.

**Donc :**

👉 **Correction 1** : applique `login_required` à la *home* :

```python
@login_required
def home_page(request):
    return render(request, "home.html")
