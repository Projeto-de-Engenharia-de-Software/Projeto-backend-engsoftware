"""
URL configuration for nexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import routers
from accounts.api_views import UserProfileAPIView, RegistrationAPIView, UserUpdateAPIView, UserDeleteAPIView, ChangePasswordView
from dashboard.api_views import RegistroViolenciaViewSet
from equipes.api_views import EquipeViewSet
from rest_framework.authtoken import views as authtoken_views

## Routers para API e troca de dados, com todos o serializers dos apps.
router = routers.DefaultRouter()
router.register(r'profiles', UserProfileAPIView, basename='profile')
router.register(r'registro-violencia', RegistroViolenciaViewSet, basename='registro-violencia')
router.register(r'equipes', EquipeViewSet, basename='equipe')

urlpatterns = [
    ## admin - Accounts(Registros e logins) - dashboard
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('dashboard/', include('dashboard.urls')), 
    path ('equipes/', include('equipes.urls')),

    # URLs da API REST Framework
    path('api/', include(router.urls)), # Inclui todas as URLs geradas pelo router, que tá lá em cima
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/', authtoken_views.obtain_auth_token, name='obtain_auth_token'),
    path('api/register/', RegistrationAPIView.as_view(), name='api_register'),
    path('api/profile/update/', UserUpdateAPIView.as_view(), name='api_profile_update'),
    path('api/profile/delete/', UserDeleteAPIView.as_view(), name='api_profile_delete'),
    path('api/profile/change-password/', ChangePasswordView.as_view(), name='api_change_password'),
]
