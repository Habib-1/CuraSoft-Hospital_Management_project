from rest_framework import serializers
from .models import service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = '__all__'
