import os
from supabase import create_client
from llama_index.embeddings.gemini import GeminiEmbedding

# 1. Conexión a Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

def buscar_ubicacion_semantica(pregunta):
    """
    Recibe la pregunta de Angular, la vectoriza y consulta a Supabase.
    """
    # Usar GeminiEmbedding para emparejar la dimensionalidad (3072) esperada por la base de datos
    embed_model = GeminiEmbedding(
        api_key=os.environ.get("GEMINI_API_KEY"), 
        model_name="models/gemini-embedding-001"
    )
    
    vector_pregunta = embed_model.get_text_embedding(pregunta)

    # Llamar a la función RPC en Supabase
    respuesta = supabase.rpc(
        'buscar_ubicaciones_local',
        {
            'query_embedding': vector_pregunta,
            'match_threshold': 0.2,
            'match_count': 3
        }
    ).execute()

    return respuesta.data
