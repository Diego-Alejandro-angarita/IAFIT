from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .services import consultar_rag, indexar_documento


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


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event

def event_list(request):
    today = timezone.now().date()
    vista = request.GET.get('vista', 'hoy')
    fecha_especifica = request.GET.get('fecha', '')

    if fecha_especifica:
        try:
            from datetime import datetime
            fecha = datetime.strptime(fecha_especifica, '%Y-%m-%d').date()
            eventos = Event.objects.filter(event_date=fecha).order_by('event_time')
            vista = 'fecha'
        except ValueError:
            eventos = Event.objects.filter(event_date=today).order_by('event_time')
            vista = 'hoy'
    elif vista == 'semana':
        from datetime import timedelta
        fin = today + timedelta(days=7)
        eventos = Event.objects.filter(event_date__gte=today, event_date__lte=fin).order_by('event_date', 'event_time')
    elif vista == 'todos':
        eventos = Event.objects.filter(event_date__gte=today).order_by('event_date', 'event_time')
    else:
        eventos = Event.objects.filter(event_date=today).order_by('event_time')
        vista = 'hoy'

    events_by_date = {}
    for event in eventos:
        date_key = event.event_date
        if date_key not in events_by_date:
            events_by_date[date_key] = []
        events_by_date[date_key].append(event)

    context = {
        'events_by_date': events_by_date,
        'today': today,
        'vista': vista,
        'fecha_especifica': fecha_especifica,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})