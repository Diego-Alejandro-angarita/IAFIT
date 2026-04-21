import os
import re
from urllib.parse import urlparse
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from google import genai

# ── Configurar Gemini ──────────────────────────────────────
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


# ── Semilleros de Investigación ────────────────────────────

SEEDBED_KEYWORDS = [
    'semillero', 'semilleros', 'investigación', 'investigacion',
    'tutor', 'tutores', 'coordinador', 'profesor',
    'facultad', 'escuela', 'grupo de investigación',
    'seedbed', 'research group', 'investigar',
]

def es_pregunta_sobre_semilleros(query: str) -> bool:
    """Detecta si la pregunta está relacionada con semilleros de investigación."""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in SEEDBED_KEYWORDS)


def buscar_semilleros_relevantes(query: str):
    """
    Busca semilleros relevantes en la base de datos según la query.
    Retorna una lista de semilleros que coinciden con la búsqueda.
    """
    from research.models import Seedbed
    from django.db.models import Q
    
    query_lower = query.lower()
    
    # Extraer términos de búsqueda relevantes
    palabras = re.findall(r'\w+', query_lower)
    palabras_relevantes = [p for p in palabras if len(p) > 3 and p not in ['sobre', 'cuales', 'cuáles', 'donde', 'como', 'qué', 'que', 'hay', 'tiene', 'tienen', 'esta', 'están', 'estan', 'puedo', 'quiero', 'necesito']]
    
    # Si pregunta por todos los semilleros
    if any(t in query_lower for t in ['todos los semilleros', 'lista de semilleros', 'cuantos semilleros', 'cuántos semilleros', 'semilleros disponibles', 'semilleros activos']):
        return list(Seedbed.objects.filter(status='ACTIVE')[:20])  # Limitar a 20 para no sobrecargar
    
    # Si pregunta por una facultad específica
    facultades_keywords = {
        'administración': 'Administración',
        'administracion': 'Administración',
        'derecho': 'Derecho',
        'ingeniería': 'Ciencias Aplicadas e Ingeniería',
        'ingenieria': 'Ciencias Aplicadas e Ingeniería',
        'ciencias': 'Ciencias Aplicadas e Ingeniería',
        'artes': 'Artes y Humanidades',
        'humanidades': 'Artes y Humanidades',
        'finanzas': 'Finanzas, Economía y Gobierno',
        'economía': 'Finanzas, Economía y Gobierno',
        'economia': 'Finanzas, Economía y Gobierno',
        'gobierno': 'Finanzas, Economía y Gobierno',
    }
    
    for keyword, faculty in facultades_keywords.items():
        if keyword in query_lower:
            return list(Seedbed.objects.filter(status='ACTIVE', faculty=faculty))
    
    # Búsqueda general por nombre, descripción o tutor
    q_filter = Q()
    for palabra in palabras_relevantes:
        q_filter |= Q(name__icontains=palabra)
        q_filter |= Q(description__icontains=palabra)
        q_filter |= Q(tutor__icontains=palabra)
    
    if q_filter:
        resultados = Seedbed.objects.filter(status='ACTIVE').filter(q_filter).distinct()[:10]
        if resultados.exists():
            return list(resultados)
    
    # Si no encuentra nada específico, retornar algunos semilleros como contexto general
    return list(Seedbed.objects.filter(status='ACTIVE')[:5])


def formatear_semilleros_para_contexto(semilleros) -> str:
    """Formatea los semilleros como texto para pasarlos al LLM."""
    if not semilleros:
        return "No se encontraron semilleros que coincidan con la búsqueda."
    
    texto = f"Se encontraron {len(semilleros)} semillero(s) de investigación:\n\n"
    
    for i, s in enumerate(semilleros, 1):
        texto += f"**{i}. {s.name}**\n"
        texto += f"   - Facultad: {s.faculty}\n"
        texto += f"   - Tutor/Coordinador: {s.tutor}\n"
        if s.description and s.description != "Description not available yet.":
            desc_corta = s.description[:300] + "..." if len(s.description) > 300 else s.description
            texto += f"   - Descripción: {desc_corta}\n"
        if s.source_url:
            texto += f"   - Más información: {s.source_url}\n"
        texto += "\n"
    
    return texto


def consultar_semilleros_con_llm(query: str) -> str:
    """
    Consulta los semilleros en la base de datos y genera una respuesta
    natural usando Gemini LLM.
    """
    # Buscar semilleros relevantes
    semilleros = buscar_semilleros_relevantes(query)
    contexto = formatear_semilleros_para_contexto(semilleros)
    
    # Obtener estadísticas generales
    from research.models import Seedbed
    from django.db.models import Count
    
    total_semilleros = Seedbed.objects.filter(status='ACTIVE').count()
    por_facultad = Seedbed.objects.filter(status='ACTIVE').values('faculty').annotate(total=Count('id')).order_by('-total')
    
    estadisticas = f"\n\nEstadísticas generales de EAFIT:\n"
    estadisticas += f"- Total de semilleros activos: {total_semilleros}\n"
    estadisticas += "- Distribución por facultad:\n"
    for f in por_facultad:
        estadisticas += f"  • {f['faculty']}: {f['total']} semilleros\n"
    
    # Crear prompt para el LLM
    system_prompt = """Eres el Asistente Virtual IAFIT de la Universidad EAFIT. Tu rol es ayudar a estudiantes 
y profesores con información sobre los semilleros de investigación de la universidad.

Responde de manera amigable, clara y en español. Si la información proporcionada es relevante, 
úsala para dar una respuesta completa. Si el usuario pregunta algo que no está en los datos, 
indícalo amablemente y sugiere cómo pueden obtener más información.

Cuando menciones semilleros, incluye detalles útiles como el nombre, facultad, tutor y una breve descripción.
"""
    
    user_prompt = f"""Pregunta del usuario: {query}

Información disponible sobre semilleros de EAFIT:
{contexto}
{estadisticas}

Por favor, responde la pregunta del usuario basándote en la información proporcionada."""

    # Llamar al LLM
    try:
        respuesta = Settings.llm.complete(
            prompt=user_prompt,
            system_prompt=system_prompt
        )
        return str(respuesta)
    except Exception as e:
        # Si falla el LLM, devolver los datos formateados directamente
        return f"Aquí está la información sobre semilleros:\n\n{contexto}"


# ── Vector Store ───────────────────────────────────────────
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
        table_name="info_directorio",
        embed_dim=3072 # models/gemini-embedding-001 output dimension expected by LlamaIndex
    )

# ── RAG ────────────────────────────────────────────────────
from .ia_service import buscar_ubicacion_semantica

from llama_index.core import PromptTemplate

QA_PROMPT = PromptTemplate(
    "Eres el asistente virtual de la Universidad EAFIT, llamado IAFIT.\n"
    "Aquí tienes algo de contexto extraído de nuestra base de datos (actualmente enfocado en el directorio de profesores):\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Si la pregunta del usuario está relacionada con el contexto, respóndela basándote en la información dada.\n"
    "Si la pregunta es un saludo (hola, buenos días, quién eres) o cualquier otro tema general que no esté en el contexto, "
    "ESTÁS AUTORIZADO a usar tus conocimientos generales como IA para responder de forma amable y servicial en español, "
    "sin decir frases limitantes como 'I cannot answer that based on the provided context'. "
    "Nunca reveles al usuario si sacaste la info del contexto o de tus conocimientos, simplemente da una respuesta directa.\n"
    "Pregunta del usuario: {query_str}\n"
    "Respuesta de IAFIT:"
)

def consultar_rag(query: str):
    vector_store = _get_vector_store()
    indice = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model
    )
    
    motor_consulta = indice.as_query_engine(
        llm=Settings.llm, 
        embed_model=Settings.embed_model,
        text_qa_template=QA_PROMPT
    )
    respuesta = motor_consulta.query(query)
    
    return str(respuesta)

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

# ── Eventos IA ───────────────────────────────────────────
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