from django.urls import path
from . import views

# urlpatterns = [
#     path("", views.gestor_home_view),
#     path("config/", views.gestor_config_view),
#     path("boletim/", views.gestor_boletim_view),
#     path("grupo/", views.gestor_grupo_view),
#     path("add_grupo/", views.gestor_add_grupo_view),
#     path("rmv_grupo/", views.gestor_rmv_grupo_view),
#     path("att_grupo/", views.gestor_att_grupo_view),
# ]


urlpatterns = [
    path('', views.gestor_home_view, name='gestor_home'),
    path('config/', views.gestor_config_view, name='gestor_config'),
    path('boletim/', views.gestor_boletim_view, name='gestor_boletim'),
    path('equipe/', views.gestor_grupo_view, name='gestor_equipe'),
    path('equipe/add/', views.gestor_add_grupo_view, name='gestor_add_equipe'),
    path('equipe/remove/', views.gestor_rmv_grupo_view, name='gestor_rmv_equipe'),
]
