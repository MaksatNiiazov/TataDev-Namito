from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords didn't match.")
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        return CustomUser.objects.create_user(**validated_data)


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        
        attrs['user'] = user
        return attrs


class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'birth_date', 'profile_picture', 'phone_number']
