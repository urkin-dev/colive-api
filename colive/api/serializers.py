from .models import Tag
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Room, Place, City, Tag, Amenity, Interest


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    amenities = AmenitySerializer(many=True)

    def get_photos(self, obj):
        if obj.photos:
            photo_urls = obj.photos.split(',')
            photo_urls = [url.strip()
                          for url in photo_urls]  # Remove empty spaces
            print(obj.place, obj.name, photo_urls)
            return photo_urls
        return []

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
        photo_urls = [photo.strip() for photos in room_photos for photo in photos.split(
            ',') if photo.strip()]

        return photo_urls

    def get_amenities(self, place):
        room_amenities = place.rooms.values_list('amenities', flat=True)
        return AmenitySerializer(Amenity.objects.filter(id__in=room_amenities), many=True).data

    class Meta:
        model = Place
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    interests = InterestsSerializer(many=True)
    city = serializers.SerializerMethodField()

    def get_city(self, user):
        return user.city.name if user.city else None

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone',
                  'phone_verification_status', 'email_verification_status', 'is_staff', 'age', 'gender', 'city', 'interests', 'bio']
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
