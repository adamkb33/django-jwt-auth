from rest_framework import serializers

from apps.common.validation import validate_norwegian_mobile_number
from apps.users.models import User


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    mobile_number = serializers.CharField(max_length=8, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'mobile_number']

    def __init__(self, *args, **kwargs):
        super(CompleteRegistrationSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email=attrs.get('email'))
            if self.user.is_verified:
                raise serializers.ValidationError("User is already verified")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with that mobile number already exists")

        if User.objects.filter(mobile_number=attrs.get('mobile_number', '')).exists():
            raise serializers.ValidationError("User with that mobile number already exists")

        mobile_number = attrs.get('mobile_number', '')
        if not validate_norwegian_mobile_number(mobile_number=mobile_number):
            raise serializers.ValidationError("The mobile number is not a valid Norwegian mobile number.")

        return attrs

    def create(self, validated_data):
        self.user.mobile_number = validated_data.get('mobile_number', '')
        self.user.save()

        return self.user
