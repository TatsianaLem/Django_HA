"""
URL configuration for test_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from first_app.views import django_greetings, user_greetings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Task Manager API',
        default_version='v1',
        description='API для менеджера задач',
    ),
    # public=False,
    # permission_classes=[permissions.IsAdminUser],
    # authentication_classes=[],
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greetings/', django_greetings, name='django_greetings'),
    path('greetings_hello/<str:name>', user_greetings),

    path('api/', include('task_manager.urls')),
    path('auth-login-jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]

# http://127.0.0.1:8000
# http://127.0.0.1:8000/admin -> urlpatterns[admin.site.urls]
# http://127.0.0.1:8000/greetings -> django_greetings(REQUEST OBJECT)
# http://127.0.0.1:8000/greetings-f-str -> user_greetings(REQUEST OBJECT)