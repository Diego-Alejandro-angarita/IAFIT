import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

def configure_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno.")

    Settings.llm = Gemini(api_key=api_key, model_name="models/gemini-2.5-flash")
    Settings.embed_model = GeminiEmbedding(api_key=api_key, model_name="models/gemini-embedding-001")
    
# Configurar Gemini al cargar el modulo
try:
    configure_gemini()
except Exception as e:
    print(f"Advertencia: No se pudo configurar Gemini: {e}")

from urllib.parse import urlparse
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore

def _get_vector_store():
    # Parse the Supabase DB URL
    db_url = os.environ.get("SUPABASE_DB_URL")
    if not db_url:
        raise ValueError("SUPABASE_DB_URL no está definido.")
        
    parsed = urlparse(db_url)
    
    return PGVectorStore.from_params(
        database=parsed.path[1:],
        host=parsed.hostname,
        password=parsed.password,
        port=parsed.port or 5432,
        user=parsed.username,
        table_name="info_directorio",
        embed_dim=3072 # models/gemini-embedding-001 output dimension expected by LlamaIndex
    )

def consultar_rag(query: str):
    vector_store = _get_vector_store()
    indice = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model
    )
    
    motor_consulta = indice.as_query_engine(llm=Settings.llm, embed_model=Settings.embed_model)
    respuesta = motor_consulta.query(query)
    
    return str(respuesta)

def indexar_documento(texto: str):
    vector_store = _get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    documentos = [Document(text=texto)]
    # Si la tabla o la extensión vector no existen, LlamaIndex intentará crearlas al instanciar o ingestar
    indice = VectorStoreIndex.from_documents(
        documentos,
        storage_context=storage_context,
        embed_model=Settings.embed_model,
        show_progress=True
    )
    return True

import psycopg2

def obtener_directorio():
    db_url = os.environ.get("SUPABASE_DB_URL")
    if not db_url:
        return []
        
    parsed = urlparse(db_url)
    
    try:
        conn = psycopg2.connect(
            dbname=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432
        )
        cur = conn.cursor()
        cur.execute("SELECT text FROM data_info_directorio LIMIT 1000;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        profesores = []
        for row in rows:
            texto = row[0]
            if "Profesor:" in texto and "Títulos:" in texto:
                partes = texto.split("Títulos:")
                nombre = partes[0].replace("Profesor:", "").strip().rstrip(".")
                titulos = partes[1].strip().rstrip(".")
                profesores.append({
                    "nombre": nombre,
                    "titulos": titulos
                })
        
        # Ordenar alfabéticamente
        profesores.sort(key=lambda x: x["nombre"])
        return profesores
    except Exception as e:
        print(f"Error extrayendo directorio: {e}")
        return []
