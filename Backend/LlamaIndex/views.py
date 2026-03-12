from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .services import (
    consultar_rag, 
    indexar_documento, 
    es_pregunta_sobre_semilleros,
    consultar_semilleros_con_llm
)

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
            
            if not query:
                return JsonResponse({'error': 'El campo "query" es requerido.'}, status=400)
            
            # Detectar si es pregunta sobre semilleros
            if es_pregunta_sobre_semilleros(query):
                respuesta = consultar_semilleros_con_llm(query)
                fuente = 'semilleros'
            else:
                # Consultar base de vectores (RAG general)
                try:
                    respuesta = consultar_rag(query)
                    fuente = 'rag'
                except Exception as rag_error:
                    # Si falla el RAG, intentar con semilleros como fallback
                    print(f"RAG error, trying seedbeds: {rag_error}")
                    respuesta = consultar_semilleros_con_llm(query)
                    fuente = 'semilleros_fallback'
            
            return JsonResponse({
                'respuesta': respuesta,
                'fuente': fuente
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
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
            return JsonResponse({'mensaje': 'Documento indexado correctamente en Supabase.'}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
