from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        # Use the custom create_user method from your UserManager
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(created_by=user)
        return user
        
