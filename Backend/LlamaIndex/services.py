import os
from urllib.parse import urlparse
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from google import genai

# ── Configurar Gemini (igual que tu compañero) ──────────────
def configure_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no encontrada.")
    Settings.llm = Gemini(api_key=api_key, model_name="models/gemini-2.5-flash")
    Settings.embed_model = GeminiEmbedding(api_key=api_key, model_name="models/gemini-embedding-001")

try:
    configure_gemini()
except Exception as e:
    print(f"Advertencia: No se pudo configurar Gemini: {e}")

# ── Vector Store (igual que tu compañero) ───────────────────
def _get_vector_store():
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
        table_name="eafit_knowledge",
        embed_dim=3072
    )

# ── RAG (igual que tu compañero) ────────────────────────────
def consultar_rag(query: str):
    vector_store = _get_vector_store()
    indice = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model
    )
    motor = indice.as_query_engine(llm=Settings.llm, embed_model=Settings.embed_model)
    return str(motor.query(query))

# ── Indexar (igual que tu compañero) ────────────────────────
def indexar_documento(texto: str):
    vector_store = _get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        [Document(text=texto)],
        storage_context=storage_context,
        embed_model=Settings.embed_model,
        show_progress=True
    )
    return True

# ── Eventos IA (tu función original, sin cambios) ───────────
from datetime import date

from datetime import date

def consultar_eventos_ia(query: str, eventos_contexto: list[dict]) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    hoy = date.today().strftime('%Y-%m-%d')
    contexto = "\n".join([
        f"- {e.get('title')} | Fecha: {e.get('event_date')} | Hora: {e.get('event_time')} | Lugar: {e.get('location')}"
        for e in eventos_contexto
    ])
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"""Eres el asistente virtual de la Universidad EAFIT llamado IAFIT.
Hoy es {hoy} (formato YYYY-MM-DD).

Tienes acceso a la lista completa de eventos próximos del campus.
Responde cualquier pregunta sobre eventos de forma clara y amigable en español.

Puedes responder preguntas como:
- ¿Qué eventos hay hoy / esta semana / en tal fecha?
- ¿A qué hora es tal evento?
- ¿Dónde es tal evento?
- ¿Hay algún evento a las X horas?
- ¿De qué trata tal evento?
- ¿Cuántos eventos hay esta semana?

Si no hay eventos que coincidan con la pregunta, dilo claramente.
Si la pregunta no es sobre eventos, responde amablemente que solo puedes ayudar con información de eventos del campus.

Lista de eventos:
{contexto}

Pregunta: {query}"""
    )
    return response.text