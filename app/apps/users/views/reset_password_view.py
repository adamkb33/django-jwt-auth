from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers.reset_password_serializer import ResetPasswordSerializer


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
