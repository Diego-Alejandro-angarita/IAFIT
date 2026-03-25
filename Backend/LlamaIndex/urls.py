from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list_api, name='event_list'),
    path('events/<int:pk>/', views.event_detail_api, name='event_detail'),
    path('api/events/', views.event_list_api, name='api_event_list'),
    path('api/query/', views.query_llama_index, name='query'),
    path('api/query', views.query_llama_index, name='query_noslash'),
    path('api/index/', views.index_document, name='index'),
    path('api/ask/', views.ask_about_events, name='ask_events'),
    path('buscar/', views.buscar_campus, name='buscar_campus'),
    path('directorio/', views.get_directory, name='get_directory'),
    path('buscar/', views.buscar_campus, name='buscar_campus'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/buscar/', views.buscar_calendario, name='buscar_calendario'),
]