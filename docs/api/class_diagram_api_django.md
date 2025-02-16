+---------------------------+
|        Utilisateur        |
+---------------------------+
| - id: Integer             |
| - nom: String             |
| - email: String           |
| - date_inscription: Date  |
+---------------------------+
            |
            | 1
            |
            | N
            v
+---------------------------+
|       Conversation        |
+---------------------------+
| - id: Integer             |
| - utilisateur_id: Integer |
| - date_creation: Date     |
+---------------------------+
            |
            | 1
            |
            | N
            v
+---------------------------+
|          Message          |
+---------------------------+
| - id: Integer             |
| - conversation_id: Integer|
| - contenu: Text           |
| - date_envoi: Date        |
+---------------------------+
