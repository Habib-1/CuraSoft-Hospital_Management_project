from django.urls import path, include
from .views import ServiceViewSet
from rest_framework.routers import DefaultRouter
roter=DefaultRouter()
roter.register('',ServiceViewSet)
urlpatterns = [
    path('', include(roter.urls)),
]