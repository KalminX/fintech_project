from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, TwoFAEnableView, OTPGenerateView, OTPVerifyView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/enable_2fa/', TwoFAEnableView.as_view(), name='2fa-enable'),
    path('auth/generate_otp/', OTPGenerateView.as_view(), name='generate-otp'),
    path('auth/verify_otp/', OTPVerifyView.as_view(), name='verify-otp')
]
