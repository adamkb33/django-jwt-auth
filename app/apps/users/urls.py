from django.urls import path

from apps.users.views.confirm_password_view import ConfirmPasswordView
from apps.users.views.partial_registration_view import PartialRegistrationView
from apps.users.views.login_view import LoginView
from apps.users.views.reset_password_view import ResetPasswordView
from apps.users.views.complete_registration_view import CompleteRegistrationView
from apps.users.views.verify_mobile_number import VerifyMobileNumberView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('register/partial/', PartialRegistrationView.as_view(), name='register-partial'),
    path('register/complete/', CompleteRegistrationView.as_view(), name='register-complete'),
    path('verify/mobile-number/', VerifyMobileNumberView.as_view(), name='verify'),

    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/', ConfirmPasswordView.as_view(), name='password-reset-confirm'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
