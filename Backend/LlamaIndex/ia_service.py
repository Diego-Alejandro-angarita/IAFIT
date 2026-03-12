import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    print("WARNING: SUPABASE_URL or SUPABASE_SERVICE_KEY is missing from .env. Supabase client will fail.")

# 1. Conexión a Supabase
supabase = create_client(supabase_url or "", supabase_key or "")

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
