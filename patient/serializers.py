from rest_framework import serializers
from .models import patient

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model=patient
        fields="__all__"


    