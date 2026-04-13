import os
from supabase import create_client
import google.generativeai as genai

# Lazy initialization to avoid crashes when env vars are not set
_supabase = None
_gemini_configured = False

# Mapeo de palabras clave en la pregunta → actividades que deben priorizarse
_KEYWORD_BOOST = {
    'inscri': ['Formulario de inscripción pregrado'],
    'admisi': ['Formulario de inscripción pregrado'],
    'ingres': ['Formulario de inscripción pregrado'],
    'matrícula': ['Pago de matrícula estudiantes nuevos'],
    'matricula': ['Pago de matrícula estudiantes nuevos'],
    'pagar': ['Pago de matrícula estudiantes nuevos'],
    'pago': ['Pago de matrícula estudiantes nuevos'],
    'clase': ['Inicio de clases'],
    'empiezan las': ['Inicio de clases'],
    'terminan las': ['Inicio de clases'],
    'acaban las': ['Inicio de clases'],
    'examen': ['Evaluaciones finales'],
    'exámen': ['Evaluaciones finales'],
    'final': ['Evaluaciones finales'],
    'parcial': ['Evaluaciones finales'],
    'evaluaci': ['Evaluaciones finales'],
    'materia': ['Registro de materias'],
    'registr': ['Registro de materias'],
    'asignatura': ['Registro de materias'],
    'prerrequisito': ['Solicitud levantamiento de requisitos'],
    'requisito': ['Solicitud levantamiento de requisitos'],
    'levantamiento': ['Solicitud levantamiento de requisitos'],
}

_BOOST_VALUE = 0.15


def _apply_keyword_boost(pregunta, resultados):
    """
    Boost de similitud para eventos cuya actividad coincida con palabras clave
    detectadas en la pregunta del usuario.
    """
    pregunta_lower = pregunta.lower()
    actividades_boost = set()

    for keyword, actividades in _KEYWORD_BOOST.items():
        if keyword in pregunta_lower:
            actividades_boost.update(actividades)

    if not actividades_boost:
        return resultados

    for r in resultados:
        if r.get('actividad') in actividades_boost:
            r['similitud'] = r.get('similitud', 0) + _BOOST_VALUE

    return resultados

def _get_supabase():
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL y SUPABASE_SERVICE_KEY deben estar configurados en .env")
        _supabase = create_client(url, key)
    return _supabase

def _configure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY debe estar configurada en .env")
        genai.configure(api_key=api_key)
        _gemini_configured = True

def _generar_embedding(texto):
    _configure_gemini()
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=texto
    )
    return result['embedding']

def buscar_ubicacion_semantica(pregunta):
    """
    Recibe la pregunta de Angular, la vectoriza y consulta a Supabase.
    """
    vector_pregunta = _generar_embedding(pregunta)

    respuesta = _get_supabase().rpc(
        'buscar_ubicaciones_local',
        {
            'query_embedding': vector_pregunta,
            'match_threshold': 0.2,
            'match_count': 3
        }
    ).execute()

    return respuesta.data


def listar_calendario():
    """
    Retorna todos los eventos del calendario académico ordenados por fecha_inicio.
    """
    respuesta = _get_supabase().table('calendario_academico') \
        .select('id,actividad,descripcion,dirigido_a,fecha_inicio,fecha_fin,periodo') \
        .order('fecha_inicio') \
        .execute()
    return respuesta.data


def buscar_evento_semantico(pregunta):
    """
    Búsqueda semántica sobre calendario_academico usando buscar_eventos RPC.
    Aplica filtrado por umbral de similitud, boost por keywords y selecciona
    solo los resultados realmente relevantes a la pregunta.
    """
    vector_pregunta = _generar_embedding(pregunta)

    respuesta = _get_supabase().rpc(
        'buscar_eventos',
        {
            'query_embedding': vector_pregunta,
            'match_count': 5
        }
    ).execute()

    resultados = respuesta.data or []

    # Filtrar por umbral mínimo de similitud
    resultados = [r for r in resultados if r.get('similitud', 0) >= 0.25]

    if not resultados:
        return []

    # Aplicar boost por palabras clave detectadas en la pregunta
    resultados = _apply_keyword_boost(pregunta, resultados)

    # Ordenar por similitud descendente (post-boost)
    resultados.sort(key=lambda r: r.get('similitud', 0), reverse=True)

    # Mantener solo resultados cercanos al mejor match (dentro de 0.08 del top)
    mejor = resultados[0]['similitud']
    resultados = [r for r in resultados if r['similitud'] >= mejor - 0.08]

    return resultados
def consultar_eventos_ia(pregunta, eventos_contexto):
    _configure_gemini()
    prompt = f"""
Eres un asistente de IAFIT. Responde la siguiente pregunta sobre los eventos basándote ÚNICAMENTE en este contexto:
{eventos_contexto}

Pregunta: {pregunta}
"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text
