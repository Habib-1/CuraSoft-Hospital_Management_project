from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PatientSerializer
from .models import patient

class PatientViewSet(viewsets.ModelViewSet):
    queryset=patient.objects.all()
    serializer_class=PatientSerializer
