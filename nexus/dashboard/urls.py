from django.urls import path
from . import views

## Por agora, não vai possuir nada, é um app puramente requisitivo para dados
urlpatterns = [
    path("", views.dashboard_home_view),
]