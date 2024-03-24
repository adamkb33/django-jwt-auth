from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.common.functions import generate_six_digit_number
from apps.common.services import SmsService
from apps.users.models import OneTimeCode
from apps.users.serializers.complete_registration_serializer import CompleteRegistrationSerializer
from core import settings


class CompleteRegistrationView(GenericAPIView):
    serializer_class = CompleteRegistrationSerializer

    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            validated_data = {
                'email': user.email,
                'given_name': user.given_name,
                'family_name': user.family_name,
                'mobile_number': user.mobile_number,
            }

            otc = generate_six_digit_number()
            if settings.DEBUG:
                otc = '123456'

            if not settings.DEBUG:
                SmsService.send_otc(recipient=validated_data['mobile_number'], otc=otc)

            OneTimeCode.objects.create(user=user, otc=otc)

            return Response({
                'data': validated_data,
                'message': 'Verification code has been sent to your mobile number.'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
