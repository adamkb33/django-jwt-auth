from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers.partial_registration_serializer import PartialRegistrationSerializer


class PartialRegistrationView(GenericAPIView):
    serializer_class = PartialRegistrationSerializer

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
            }

            return Response({
                'data': validated_data,
                'message': 'Partial user is created.'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
