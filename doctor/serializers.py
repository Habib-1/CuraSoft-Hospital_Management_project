from rest_framework import serializers
from .import models

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    designation = serializers.StringRelatedField(many=True)
    specializations= serializers.StringRelatedField(many=True)
    available_time = serializers.StringRelatedField(many=True)
    class Meta:
        model=models.doctor
        fields="__all__"

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.designation
        fields="__all__"

class Available_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.available_time
        fields="__all__"

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.specialization
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.review
        fields="__all__"