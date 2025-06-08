from django.urls import path
from . import views

urlpatterns = [
    path('', views.pds_home_view),
    path('boletim/', views.pds_boletim_view),
    path('config/', views.pds_config_view),
    path('grupo/', views.pds_grupo_view)
]