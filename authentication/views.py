import os

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dotenv import load_dotenv

load_dotenv()


class GoogleLogin(SocialLoginView):
    """Takes care of exchanging the authorization code provided by the Google Server for an access token.

    Returns the token.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get('GOOGLE_LOGIN_CALLBACK_URL')
    client_class = OAuth2Client
