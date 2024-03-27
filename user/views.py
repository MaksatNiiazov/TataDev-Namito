from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (
    CustomUserSerializer, 
    VerifyCodeSerializer,
    )
from .utils import (
    send_sms, 
    generate_confirmation_code,
    )


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_user = CustomUser.objects.filter(phone_number=phone_number).exists()
        if existing_user:
            return Response({'error': 'User with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = generate_confirmation_code()

        user = CustomUser.objects.create(phone_number=phone_number, code=confirmation_code)
        serializer = CustomUserSerializer(user)

        send_sms(phone_number, confirmation_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = VerifyCodeSerializer  

    def create(self, request, *args, **kwargs):
        code = request.data.get('code')

        if not code:
            return Response({'error': 'Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(code=code).first()
        if not user:
            return Response({'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()

        # Создание и выдача токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
