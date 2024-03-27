from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number')


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
