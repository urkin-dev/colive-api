from django.urls import path
from .views import LoginView, SignupView, UserExistsView, CurrentUserView, CityListView, SuggestedCityView, SearchPlaceView, SearchPlacesView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('users/exists/', UserExistsView.as_view(), name='exists'),
    path('users/', CurrentUserView.as_view(), name='users'),
    path('city/', CityListView.as_view()),
    path('suggest/', SuggestedCityView.as_view()),
    path('places/<int:id>/', SearchPlaceView.as_view()),
    path('places/', SearchPlacesView.as_view()),
]
