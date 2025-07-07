# spignosapi/api/advise/urls.py
from django.urls import path
from .views import ReconversionAdviceView

urlpatterns = [
    path("reconversion/", ReconversionAdviceView.as_view(), name="reconversion_advice"),
]
