from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'establishments', views.EstablishmentViewSet, basename='establishment')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'menus', views.MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('events/', views.event_list_api, name='event_list'),
    path('events/<int:pk>/', views.event_detail_api, name='event_detail'),
    path('events/', views.event_list_api, name='api_event_list'),
    path('query/', views.query_llama_index, name='query'),
    path('index/', views.index_document, name='index_document'),
    path('ask/', views.ask_about_events, name='ask_events'),
    path('buscar/', views.buscar_campus, name='buscar_campus'),
    path('directorio/', views.get_directory, name='get_directory'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/buscar/', views.buscar_calendario, name='buscar_calendario'),
    path('semilleros/', views.query_semilleros, name='query_semilleros'),
]
