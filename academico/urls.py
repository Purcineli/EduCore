from django.urls import path

from . import views

app_name = 'academico'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
