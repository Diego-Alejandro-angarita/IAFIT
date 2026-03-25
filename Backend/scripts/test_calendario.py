import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# =============================
# CARGAR VARIABLES DE ENTORNO
# =============================

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

# =============================
# CARGAR MODELO DE EMBEDDINGS
# =============================

print("Cargando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def generar_embedding(texto):
    return model.encode(texto).tolist()

# =============================
# PREGUNTAS DE PRUEBA
# =============================

preguntas = [
    "cuando empiezan las clases",
    "cuando son las evaluaciones finales",
    "cuando se pagan las matriculas",
    "cuando puedo registrar materias"
]

# =============================
# BUSQUEDA VECTORIAL
# =============================

def buscar_evento(pregunta):

    embedding = generar_embedding(pregunta)

    response = supabase.rpc(
        "buscar_eventos",
        {
            "query_embedding": embedding,
            "match_count": 3
        }
    ).execute()

    return response.data


# =============================
# EJECUTAR PRUEBAS
# =============================

print("\n===== PRUEBAS DE BÚSQUEDA =====\n")

for pregunta in preguntas:

    print(f"\nPregunta: {pregunta}")

    resultados = buscar_evento(pregunta)

    if resultados:
        for r in resultados:
            print("Actividad:", r["actividad"])
            print("Fecha inicio:", r["fecha_inicio"])
            print("Fecha fin:", r["fecha_fin"])
            print("Similitud:", r["similitud"])
            print("---")
    else:
        print("No se encontraron resultados")

print("\nPrueba completada")