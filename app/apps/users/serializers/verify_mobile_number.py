from rest_framework import serializers

from apps.common.validation import validate_otc
from apps.users.models import OneTimeCode


class VerifyMobileNumberSerializer(serializers.Serializer):
    otc = serializers.CharField(max_length=6, min_length=6, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        if not validate_otc(otc=attrs.get('otc', '')):
            raise serializers.ValidationError("Invalid one time code.")

        try:
            otc = OneTimeCode.objects.get(otc=attrs.get('otc', ''))
        except OneTimeCode.DoesNotExist:
            raise serializers.ValidationError({"otc": "One time code is invalid."})

        user = otc.user

        return {
            'otc': attrs.get('otc', ''),
            'user_data': user.get_session()
        }
