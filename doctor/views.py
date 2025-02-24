from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class DoctorPagination(PageNumberPagination):
    page_size=2
    page_size_query_param=page_size
    max_page_size=100

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = models.doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    pagination_class=DoctorPagination

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = models.designation.objects.all()
    serializer_class = serializers.DesignationSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = models.specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.review.objects.all()
    serializer_class = serializers.ReviewSerializer

class Available_timeViewSet(viewsets.ModelViewSet):
    queryset = models.available_time.objects.all()
    serializer_class = serializers.Available_timeSerializer
