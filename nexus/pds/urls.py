from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.pds_home_view),
#     path('boletim/', views.pds_boletim_view),
#     path('config/', views.pds_config_view),
#     path('grupo/', views.pds_grupo_view)
# ]


urlpatterns = [
    path('', views.pds_home_view, name='pds_home'),
    path('config/', views.pds_config_view, name='pds_config'),
    path('boletim/', views.pds_boletim_view, name='pds_boletim'),
    path('grupo/', views.pds_equipe_view, name='pds_equipe'),
]
