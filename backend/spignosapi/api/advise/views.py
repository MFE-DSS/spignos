# spignosapi/api/advise/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from spignosapi.llm.prompts.orchestrator import Orchestrator


class ReconversionAdviceView(APIView):
    """
    Donne des conseils pour une reconversion IT en combinant plusieurs agents MCP.
    """

    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response(
                {"error": "Champ 'question' requis."}, status=status.HTTP_400_BAD_REQUEST
            )

        orchestrator = Orchestrator()
        final_answer = orchestrator.run(question)

        return Response({"answer": final_answer}, status=status.HTTP_200_OK)
