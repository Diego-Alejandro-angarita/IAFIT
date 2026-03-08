import os
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Lazy initialization to avoid crashes when env vars are not set
_supabase = None
_model = None

def _get_supabase():
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL y SUPABASE_SERVICE_KEY deben estar configurados en .env")
        _supabase = create_client(url, key)
    return _supabase

def _get_model():
    global _model
    if _model is None:
        print("Inicializando motor de búsqueda semántica...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def buscar_ubicacion_semantica(pregunta):
    """
    Recibe la pregunta de Angular, la vectoriza y consulta a Supabase.
    """
    model = _get_model()
    vector_pregunta = model.encode(pregunta).tolist()

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
    """
    model = _get_model()
    vector_pregunta = model.encode(pregunta).tolist()

    respuesta = _get_supabase().rpc(
        'buscar_eventos',
        {
            'query_embedding': vector_pregunta,
            'match_count': 5
        }
    ).execute()

    return respuesta.data
