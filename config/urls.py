from django.urls import path
from box_selector.views import health, recommend

urlpatterns = [
    path("api/health/", health),
    path("api/recommend/", recommend),
]
