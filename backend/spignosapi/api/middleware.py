from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class RateLimitedAPIView(APIView):
    @method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Erreur API : {str(e)}")
            return JsonResponse({"error": "Une erreur interne est survenue"}, status=500)
        return response
