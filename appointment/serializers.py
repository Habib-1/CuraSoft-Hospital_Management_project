from rest_framework import serializers
from .import models

class AppoinmentSerializer(serializers.ModelSerializer):
    patient=serializers.StringRelatedField(many=False)
    doctor=serializers.StringRelatedField(many=False)
    time=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.appointemt
        fields="__all__"