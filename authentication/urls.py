from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView

from authentication.views import GoogleLogin

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path("account-confirm-email/<key>/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
