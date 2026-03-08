from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .services import consultar_rag, indexar_documento
from .ia_service import buscar_ubicacion_semantica
from .models import Establishment, Category, Menu
from .serializers import (
    EstablishmentSerializer,
    EstablishmentListSerializer,
    CategorySerializer,
    MenuSerializer
)


@csrf_exempt
def query_llama_index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
            
            # Consultar base de vectores
            respuesta = consultar_rag(query)
            
            return JsonResponse({'respuesta': respuesta}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


@csrf_exempt
def index_document(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto')
            
            if not texto:
                return JsonResponse({'error': 'El campo "texto" es requerido.'}, status=400)
                
            indexar_documento(texto)
            return JsonResponse({'mensaje': 'Documento indexado correctamente en Supabase.'}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


@require_GET
def buscar_campus(request):
    """endpoints para buscar ubicaciones en el campus"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Consulta vacía'}, status=400)
    try:
        result = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultado': result}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ViewSets para la Oferta Gastronómica
class EstablishmentViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar establecimientos gastronómicos"""
    queryset = Establishment.objects.prefetch_related('categories', 'schedules', 'menus')
    serializer_class = EstablishmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description', 'location']
    filterset_fields = ['establishment_type']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EstablishmentListSerializer
        return EstablishmentSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Obtener establecimientos filtrados por categoría"""
        category_name = request.query_params.get('category', None)
        
        if not category_name:
            return Response(
                {'error': 'El parámetro "category" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            category = Category.objects.get(name=category_name)
            establishments = self.queryset.filter(categories=category)
            serializer = self.get_serializer(establishments, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {'error': f'Categoría "{category_name}" no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def open_now(self, request):
        """Obtener establecimientos que están abiertos ahora"""
        from django.utils import timezone
        
        now = timezone.now()
        today = now.isoweekday()  # 1=Lunes, 7=Domingo
        current_time = now.time()
        
        # Subquery para obtener establecimientos con horarios válidos para hoy
        from django.db.models import Q
        from .models import Schedule
        
        establishments = self.queryset.filter(
            schedules__day_of_week=today,
            schedules__is_open=True,
            schedules__opening_time__lte=current_time,
            schedules__closing_time__gt=current_time
        ).distinct()
        
        serializer = self.get_serializer(establishments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Obtener todas las categorías disponibles"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar categorías"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar menús"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['establishment']

def buscar_campus(request):
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Debes enviar una pregunta en el parámetro "q"'}, status=400)

    try:
        resultados = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultados': resultados}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
