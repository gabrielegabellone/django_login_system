"""
URL configuration for django_login_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django Login System API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


@api_view(['GET'])
def hello_world(request):
    """Endpoint for testing purposes that returns the message 'Hello {username}!' if the user is authenticated."""
    return Response({"message": f"Hello {request.user}!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('authentication.urls')),
    path('hello/', hello_world),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
]
