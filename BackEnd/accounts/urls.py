from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .models import UserProfile
from .views import RegisterView, ProfileView, LoginView, DeleteUserView, LogoutView, UserSettingsAPIView, ChangeTeamAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-user/', DeleteUserView.as_view(), name="delete-user"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('settings/', UserSettingsAPIView.as_view(), name='user-settings'),
    path('settings/change-team/', ChangeTeamAPIView.as_view(), name='change-team'),
]
