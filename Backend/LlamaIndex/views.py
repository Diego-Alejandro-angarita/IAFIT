import json
import traceback
import pytz

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import Event
from django.views.decorators.http import require_GET
from .services import consultar_rag, indexar_documento, obtener_directorio
from .ia_service import buscar_ubicacion_semantica, consultar_eventos_ia

# Zona horaria de Colombia
BOGOTA_TZ = pytz.timezone('America/Bogota')

def get_today():
    """Retorna la fecha actual en Colombia."""
    return datetime.now(BOGOTA_TZ).date()

# --- VISTAS DE IA (API) ---
from .ia_service import buscar_ubicacion_semantica, listar_calendario, buscar_evento_semantico

@csrf_exempt
def query_llama_index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            contexto = data.get('contexto', '')
            
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
                
            if contexto:
                query = f"Información adicional sobre ubicaciones o calendario encontrada en una base de datos externa:\n{contexto}\n\nAplica este contexto si la pregunta es relevante a un bloque o calendario.\nPregunta del usuario: {query}"
                
            respuesta = consultar_rag(query)
            return JsonResponse({'respuesta': respuesta}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            traceback.print_exc()
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
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Debes enviar una pregunta en el parámetro "q"'}, status=400)

    try:
        resultados = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultados': resultados}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_directory(request):
    if request.method == 'GET':
        directorio = obtener_directorio()
        return JsonResponse(directorio, safe=False, status=200)
        
    return JsonResponse({'error': 'Método no permitido. Use GET.'}, status=405)

@require_GET
def buscar_campus(request):
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Debes enviar una pregunta en el parámetro "q"'}, status=400)

    try:
        resultados = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultados': resultados}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_directory(request):
    if request.method == 'GET':
        directorio = obtener_directorio()
        return JsonResponse(directorio, safe=False, status=200)
        
    return JsonResponse({'error': 'Método no permitido. Use GET.'}, status=405)

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