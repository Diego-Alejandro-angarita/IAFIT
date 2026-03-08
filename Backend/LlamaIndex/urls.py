from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'establishments', views.EstablishmentViewSet, basename='establishment')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'menus', views.MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('query/', views.query_llama_index, name='query_llama_index'),
    path('indexar/', views.index_document, name='index_document'),
    path('buscar/', views.buscar_campus, name='buscar_campus'),
]
