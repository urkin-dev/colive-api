from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignupSerializer, CustomUserSerializer, PlaceSerializer, HotelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Place, Hotel
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        limit = request.GET.get('limit')
        if limit is not None:
            limit = int(limit)

        # Get the desired cities based on their IDs
        desired_city_ids = [9213, 124124, 123213213213]
        desired_cities = Place.objects.filter(
            type='city', cityId__in=desired_city_ids)

        # Get the remaining cities excluding the desired ones
        other_cities = Place.objects.filter(
            type='city').exclude(cityId__in=desired_city_ids)

        # Combine the desired cities and other cities
        cities = list(desired_cities) + list(other_cities)

        # Limit the number of cities if specified
        if limit is not None:
            cities = cities[:limit]

        serializer = PlaceSerializer(cities, many=True)
        return Response({'results': serializer.data})


class SuggestedPlaceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.GET.get('search')
        if search:
            places = Place.objects.filter(name__icontains=search)
        else:
            places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


class SearchPlaceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        adults = int(request.GET.get('adults'))
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        children_ages = request.GET.get(
            'children_ages') if 'children_ages' in request.GET else None

        try:
            hotel = Hotel.objects.get(id=id)
        except Hotel.DoesNotExist:
            raise Http404("Hotel does not exist")

        serializer = HotelSerializer(hotel)
        return Response(serializer.data)


class SearchPlacesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        adults = int(request.GET.get('adults'))
        city_id = int(request.GET.get('cityId')
                      ) if 'cityId' in request.GET else None
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')
        children_ages = request.GET.get('childrenAges')

        hotels = Hotel.objects.all()

        if city_id:
            hotels = hotels.filter(cityId=city_id)

        hotels = hotels.filter(rooms__limit__gte=adults)

        if children_ages:
            children_ages_list = children_ages.split(',')
            max_child_age = max([int(age) for age in children_ages_list])

            hotels = hotels.filter(rooms__children_limit__gte=max_child_age)

        hotels = hotels.distinct()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserExistsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        email = request.query_params.get('email', '')

        user_exists = CustomUser.objects.filter(email=email).exists(
        )

        return Response({'exists': user_exists})


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
