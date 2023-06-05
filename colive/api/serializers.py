from .models import Tag
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, CancellationPolicy, Room, Place, City, Tag, Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    cancellation_policy = CancellationPolicySerializer()
    photos = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()

    def get_photos(self, obj):
        if obj.photos:
            return obj.photos.split(',')
        return []

    def get_amenities(self, obj):
        amenities = obj.amenity_set.all()
        return AmenitySerializer(amenities, many=True).data

    class Meta:
        model = Room
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)
    photos = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    amenities = serializers.SerializerMethodField()

    def get_photos(self, place):
        room_photos = place.rooms.values_list('photos', flat=True)
        return [photo for photos in room_photos for photo in photos.split(',')]

    def get_amenities(self, place):
        amenities = Amenity.objects.filter(room__place=place).distinct()
        return AmenitySerializer(amenities, many=True).data

    class Meta:
        model = Place
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone',
                  'phone_verification_status', 'email_verification_status', 'is_staff']
        partial = True


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


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            password=validated_data['password']
        )

        return user
