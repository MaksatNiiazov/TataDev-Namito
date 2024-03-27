from django.urls import path
from .views import UserRegistrationView, VerifyCodeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
]
