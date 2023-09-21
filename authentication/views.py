import os

from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

load_dotenv()


class GoogleLogin(SocialLoginView):
    """Takes care of exchanging the authorization code provided by the Google Server for an access token.

    Returns the token.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get('GOOGLE_LOGIN_CALLBACK_URL')
    client_class = OAuth2Client


@api_view(['GET'])
def hello_world(request):
    """Endpoint for testing purposes that returns the message 'Hello {username}!' if the user is authenticated."""
    return Response({"message": f"Hello {request.user}!"})
