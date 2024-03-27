from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (
    CustomUserSerializer, 
    VerifyCodeSerializer,
    UserProfileSerializer
    )
from .utils import (
    send_sms, 
    generate_confirmation_code,
    )


class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерация и отправка кода подтверждения
        confirmation_code = generate_confirmation_code()
        send_sms(phone_number, confirmation_code)

        # Сохранение кода подтверждения в базе данных
        CustomUser.objects.update_or_create(
            phone_number=phone_number,
            defaults={'code': confirmation_code}
        )

        return Response({'message': 'Confirmation code sent successfully.'}, status=status.HTTP_200_OK)


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = VerifyCodeSerializer  

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if not code:
            return Response({'error': 'Сode are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка кода подтверждения
        user = CustomUser.objects.filter(code=code).first()
        if not user:
            return Response({'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Помечаем пользователя как верифицированного и сохраняем
        user.is_verified = True
        user.save()

        # Создание и выдача токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    