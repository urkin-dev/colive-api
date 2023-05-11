from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        print(request)
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
