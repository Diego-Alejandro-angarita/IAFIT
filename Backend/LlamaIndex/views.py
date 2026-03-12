import json
import traceback
import pytz

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Event
from .services import consultar_rag, indexar_documento, consultar_eventos_ia

# Zona horaria de Colombia
BOGOTA_TZ = pytz.timezone('America/Bogota')

def get_today():
    """Retorna la fecha actual en Colombia."""
    return datetime.now(BOGOTA_TZ).date()

# --- VISTAS DE IA (API) ---

@csrf_exempt
def query_llama_index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
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
        eventos = Event.objects.filter(
            event_date__gte=today
        ).order_by('event_date', 'event_time')
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