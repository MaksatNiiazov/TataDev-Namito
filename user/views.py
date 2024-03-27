from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from .utils import send_sms, generate_confirmation_code

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = generate_confirmation_code()

        send_sms(phone_number, confirmation_code)

        user = CustomUser.objects.create(phone_number=phone_number)
        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
