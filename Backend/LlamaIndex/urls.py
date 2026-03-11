from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.query_llama_index, name='query_llama_index'),
    path('indexar/', views.index_document, name='index_document'),
    path('buscar/', views.buscar_campus, name='buscar_campus'),
    path('directorio/', views.get_directory, name='get_directory'),
]
