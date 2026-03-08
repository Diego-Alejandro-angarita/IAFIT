from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .services import consultar_rag, indexar_documento
from .ia_service import buscar_ubicacion_semantica, listar_calendario, buscar_evento_semantico

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
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'error': 'Debes enviar una pregunta en el parámetro "q"'}, status=400)

    try:
        resultados = buscar_ubicacion_semantica(query)
        return JsonResponse({'resultados': resultados}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
