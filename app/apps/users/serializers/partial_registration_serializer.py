from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class PartialRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    given_name = serializers.CharField(max_length=68, min_length=2, write_only=True)
    family_name = serializers.CharField(max_length=68, min_length=2, write_only=True)

    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'given_name', 'family_name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("passwords do not match")

        if User.objects.filter(email=attrs.get('email', '')).exists():
            raise serializers.ValidationError("User with that email already exists")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            family_name=validated_data.get('family_name'),
            given_name=validated_data.get('given_name'),
            mobile_number=None,
            password=validated_data.get('password')
        )

        return user
