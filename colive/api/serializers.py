from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            raise serializers.ValidationError('Incorrect email or password')

        return user
