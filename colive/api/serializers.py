from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, CancellationPolicy, Room, Hotel, Place


class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    cancellation_policy = CancellationPolicySerializer()
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        if obj.photos:
            return obj.photos.split(',')
        return []

    class Meta:
        model = Room
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        if obj.photos:
            return obj.photos.split(',')
        return []

    class Meta:
        model = Hotel
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone',
                  'phone_verification_status', 'email_verification_status', 'is_staff']


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


class SignupSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data['phone'],
            password=validated_data['password']
        )

        return user
