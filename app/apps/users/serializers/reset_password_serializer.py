from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from django.core.mail import send_mail  # If you're sending an email
from apps.users.models import User
from core import settings


class ResetPasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=8, min_length=8, write_only=True)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(mobile_number=attrs['mobile_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User was not found")
        return attrs

    def save(self):
        user = self.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.CLIENT_URL}/auth/password-reset?uid={uid}&token={token}"
        html_message = render_to_string('emails/password-reset.html',
                                        {'company_name': settings.COMPANY_NAME, 'reset_link': reset_link})
        plain_message = strip_tags(html_message)

        subject = "Your Password Reset Link"
        from_email = settings.EMAIL_HOST_USER
        to_email = user.email

        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=html_message,
            fail_silently=False,
        )

        return {'message': 'Password reset instructions have been sent.'}
