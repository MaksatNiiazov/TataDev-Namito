from django.urls import path
from .views import CustomUserRegistrationView, CustomUserLoginView, CustomUserProfileView

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('profile/', CustomUserProfileView.as_view(), name='profile'),
]
