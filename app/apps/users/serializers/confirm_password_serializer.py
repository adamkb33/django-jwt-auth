from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.encoding import force_str

User = get_user_model()


class ConfirmPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)

    def __init__(self, *args, **kwargs):
        super(ConfirmPasswordSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({"password2": "New Password and Confirm Password doesn't match."})

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            self.user = user
        else:
            raise serializers.ValidationError({"uid": "Invalid token or UID"})

        return attrs

    def save(self, **kwargs):
        """
        Set the new password.
        """
        password = self.validated_data['password']
        user = self.user
        user.set_password(password)
        user.save()
        return user
