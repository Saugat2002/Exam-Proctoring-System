from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username', 'email', 'password', 'marks_obtained')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        student = Student.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            marks_obtained=validated_data.get('marks_obtained', 0)  # Default to 0 if not provided
        )
        return student
        
    def update(self, instance, validated_data):
        instance.marks_obtained = validated_data.get('marks_obtained', instance.marks_obtained)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


