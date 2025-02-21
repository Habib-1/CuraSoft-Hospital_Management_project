from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = models.doctor.objects.all()
    serializer_class = serializers.DoctorSerializer

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
