from rest_framework.views import APIView
from rest_framework.response import Response

class ChatAPI(APIView):
    def post(self, request):
        message = request.data.get('message', '')
        response_text = f"SPIGNOS AI Response: {message[::-1]}"  # Simulation de réponse LLM
        return Response({"response": response_text})
