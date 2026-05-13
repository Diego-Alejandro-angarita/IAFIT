import json
import traceback
import pytz

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Establishment, Category, Menu
from .services import (
    consultar_rag,
    indexar_documento,
    obtener_directorio,
    es_pregunta_sobre_correo_profesor,
    consultar_correo_profesor,
    es_pregunta_sobre_semilleros,
    consultar_semilleros_con_llm,
    consultar_eventos_ia
)
from .ia_service import buscar_ubicacion_semantica, listar_calendario, buscar_evento_semantico
from .serializers import (
    EstablishmentSerializer,
    EstablishmentListSerializer,
    CategorySerializer,
    MenuSerializer
)

# Zona horaria de Colombia
BOGOTA_TZ = pytz.timezone('America/Bogota')

def get_today():
    """Retorna la fecha actual en Colombia."""
    return datetime.now(BOGOTA_TZ).date()

# --- VISTAS DE IA (API) ---

@csrf_exempt
def query_llama_index(request):
    """
    Endpoint principal para consultas del chat.
    Detecta automáticamente si la pregunta es sobre semilleros o usa el RAG general.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            contexto = data.get('contexto', '')
            
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
            
            # Resolver correos de profesores directamente desde el directorio
            if es_pregunta_sobre_correo_profesor(query):
                respuesta = consultar_correo_profesor(query)
                fuente = 'directorio_email'
            elif es_pregunta_sobre_semilleros(query):
                respuesta = consultar_semilleros_con_llm(query)
                fuente = 'semilleros'
            else:
                # Si hay contexto de ubicaciones/calendario, enriquecer la query
                if contexto:
                    query = f"Información adicional sobre ubicaciones o calendario encontrada en una base de datos externa:\n{contexto}\n\nAplica este contexto si la pregunta es relevante a un bloque o calendario.\nPregunta del usuario: {query}"
                
                # Consultar base de vectores (RAG general)
                try:
                    respuesta = consultar_rag(query)
                    fuente = 'rag'
                except Exception as rag_error:
                    print(f"RAG error: {rag_error}")
                    respuesta = "No pude obtener la información del directorio en este momento."
                    fuente = 'rag_error'
            
            return JsonResponse({
                'respuesta': respuesta,
                'fuente': fuente
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


@csrf_exempt
def query_semilleros(request):
    """
    Endpoint específico para consultas sobre semilleros de investigación.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
            
            respuesta = consultar_semilleros_con_llm(query)
            
            return JsonResponse({
                'respuesta': respuesta,
                'fuente': 'semilleros'
            }, status=200)
            
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
            return JsonResponse({'mensaje': 'Documento indexado correctamente.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


@require_GET
def calendario(request):
    """Lista todos los eventos del calendario académico ordenados cronológicamente."""
    try:
        eventos = listar_calendario()
        return JsonResponse({'eventos': eventos}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def buscar_calendario(request):
    """Búsqueda semántica sobre el calendario académico."""
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Debes enviar una pregunta en el parámetro "q"'}, status=400)

    try:
        resultados = buscar_evento_semantico(query)
        return JsonResponse({'resultados': resultados}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def buscar_campus(request):
    """endpoints para buscar ubicaciones en el campus"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Consulta vacía'}, status=400)
    try:
        result = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultados': result}, status=200)
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



@csrf_exempt
def ask_about_events(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        eventos_contexto = data.get('contexto_eventos', [])
        if not query:
            return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
        respuesta = consultar_eventos_ia(query, eventos_contexto)
        return JsonResponse({'message_es': respuesta}, status=200)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

# --- VISTAS DEL DIRECTORIO ---

@require_GET
def get_directory(request):
    """
    Retorna la lista de profesores desde Supabase.
    """
    try:
        data = obtener_directorio()
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


# --- VISTAS DE EVENTOS (API REST) ---

def event_list_api(request):
    today = get_today()  # ← fecha correcta en Colombia
    vista = request.GET.get('vista', 'hoy')
    fecha_param = request.GET.get('fecha', '')

    if fecha_param:
        try:
            fecha = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            eventos = Event.objects.filter(event_date=fecha).order_by('event_time')
        except ValueError:
            eventos = Event.objects.filter(event_date=today).order_by('event_time')
    elif vista == 'semana':
        lunes = today - timedelta(days=today.weekday())
        domingo = lunes + timedelta(days=6)
        eventos = Event.objects.filter(
            event_date__gte=lunes,
            event_date__lte=domingo
        ).order_by('event_date', 'event_time')
    elif vista == 'todos':
        eventos = Event.objects.all().order_by('event_date', 'event_time')
    else:  # hoy
        eventos = Event.objects.filter(event_date=today).order_by('event_time')

    data = [
        {
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'location': e.location,
            'event_date': e.event_date.strftime('%Y-%m-%d'),
            'event_time': e.event_time.strftime('%H:%M'),
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)

def event_detail_api(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado.'}, status=404)

    data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'location': event.location,
        'event_date': event.event_date.strftime('%Y-%m-%d'),
        'event_time': event.event_time.strftime('%H:%M'),
    }
    return JsonResponse(data)
