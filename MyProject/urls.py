"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from Account.views import *
from rest_framework_swagger.views import get_swagger_view
from django.urls import re_path as url
from django.urls import re_path
schema_view = get_swagger_view(title='Pastebin API')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



schema_view = get_schema_view(
    openapi.Info(
        title="My project",
        default_version='v1',
        # description="Welcome to the world of MT",
        # terms_of_service="https://triazinesoft.com",
        # contact=openapi.Contact(email="jpmaurya@triazinesoft.com"),
        # license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/v1/', include('Account.urls')),
    re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
