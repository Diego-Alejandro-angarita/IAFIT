import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')

def buscar_en_campus(pregunta):
    print(f"\nBuscando: '{pregunta}'...")
    
    # 1. Convertimos la pregunta del usuario a vector
    vector_pregunta = model.encode(pregunta).tolist()
    
    # 2. Llamamos a la función de SQL que acabas de crear
    respuesta = supabase.rpc(
        'buscar_ubicaciones_local',
        {
            'query_embedding': vector_pregunta,
            'match_threshold': 0.2, # Umbral bajo para ver qué encuentra
            'match_count': 2        # Traer los 2 mejores resultados
        }
    ).execute()
    
    # 3. Mostrar resultados
    if len(respuesta.data) == 0:
        print("No se encontraron coincidencias.")
    else:
        for index, lugar in enumerate(respuesta.data):
            print(f"Resultado {index + 1} (Similitud: {lugar['similarity']:.2f}):")
            print(f" - Bloque {lugar['codigo_bloque']}, Piso {lugar['piso']}")
            print(f" - Descripción: {lugar['descripcion_semantica']}")

# ¡Prueba con diferentes frases de estudiantes!
buscar_en_campus("¿En qué piso están las aulas de clase normales?")
buscar_en_campus("Necesito ir a un laboratorio de física")
buscar_en_campus("¿Dónde puedo encontrar baños accesibles?")
