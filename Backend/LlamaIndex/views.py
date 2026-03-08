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
