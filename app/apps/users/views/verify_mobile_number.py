from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import OneTimeCode
from apps.users.serializers.verify_mobile_number import VerifyMobileNumberSerializer


class VerifyMobileNumberView(GenericAPIView):
    serializer_class = VerifyMobileNumberSerializer

    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            otc = OneTimeCode.objects.get(otc=validated_data['otc'])

            user = otc.user
            user.is_verified = True
            user.save()

            otc.delete()

            return Response({
                'data': validated_data['user_data'],
                'message': 'User is successfully registered.'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
