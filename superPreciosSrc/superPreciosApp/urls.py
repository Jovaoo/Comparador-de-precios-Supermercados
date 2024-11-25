from django.urls import path
from . import views  # Importa las vistas de la aplicación

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('producto', views.producto, name='producto'),
]
