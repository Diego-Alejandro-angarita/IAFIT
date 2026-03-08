import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

# Configuración Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

# CARGAR EL MODELO LOCAL (Se descarga solo la primera vez)
print("Cargando modelo local...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def generar_embedding_local(texto):
    # Genera el vector usando tu CPU
    return model.encode(texto).tolist()

# Datos del Bloque 20
datos_bloque_20 = [
        {
        "codigo_bloque": "20",
        "piso": 1,
        "descripcion": "Bloque 20. Cerca a los bloques 19, 13, 14, 15. Cerca a Bancolombia. Cuenta con el Laboratorio del Café" ,
        "meta": {"tipo": "laboratorios", "accesible": True}
    },
    {
        "codigo_bloque": "20",
        "piso": 2,
        "descripcion": "Bloque 20. Piso 2: Laboratorios de física. Baños para mujeres, hombres y discapacitados. Acceso por escaleras y ascensores",
        "meta": {"tipo": "laboratorios", "accesible": True}
    },
    {
        "codigo_bloque": "20",
        "piso": 3,
        "descripcion": "Bloque 20 Ciencias. Piso 3: Aulas de clase, salas de cómputo. Baños para mujeres, hombres y discapacitados Acceso por escaleras y ascensores.",
        "meta": {"baños": "estándar", "tipo": "aulas", "accesible": True}
    }
]

for item in datos_bloque_20:
    print(f"Procesando piso {item['piso']}...")
    vector = generar_embedding_local(item['descripcion'])
    
    supabase.table("ubicaciones_campus").insert({
        "codigo_bloque": item['codigo_bloque'],
        "piso": item['piso'],
        "descripcion_semantica": item['descripcion'],
        "metadatos": item['meta'],
        "embedding": vector
    }).execute()

print("¡Dataset cargado localmente!")