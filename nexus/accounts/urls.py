from django.urls import path
from . import views

# O app_name é importante para o Django saber a que app estas URLs pertencem
app_name = 'accounts'

urlpatterns = [
    # A página inicial de registo, que dá as opções
    path('register/', views.register_options_view, name='register_options'),
    
    # As rotas para os formulários de registo específicos
    path('register/gestor/', views.register_gestor_view, name='register_gestor'),
    path('register/profissional/', views.register_profissional_view, name='register_profissional'),
    
    # As rotas de login e logout
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
]
