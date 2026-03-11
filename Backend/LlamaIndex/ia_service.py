import os
from supabase import create_client
from sentence_transformers import SentenceTransformer

# 1. Conexión a Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

# 2. Cargar el modelo en memoria (Se carga una sola vez al iniciar Django)
print("Inicializando motor de búsqueda semántica...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def buscar_ubicacion_semantica(pregunta):
    """
    Recibe la pregunta de Angular, la vectoriza y consulta a Supabase.
    """
    # Convertir texto a matemáticas
    vector_pregunta = model.encode(pregunta).tolist()

    # Llamar a la función RPC que ya creaste en Supabase
    respuesta = supabase.rpc(
        'buscar_ubicaciones_local',
        {
            'query_embedding': vector_pregunta,
            'match_threshold': 0.2,
            'match_count': 3
        }
    ).execute()

    return respuesta.data
