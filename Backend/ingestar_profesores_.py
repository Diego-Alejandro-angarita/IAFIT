import urllib.request
import json
import ssl
import time

def invocar_ingesta_profesor(nombre, titulos):
    """
    Toma el nombre y los títulos de un profesor y los envía al endpoint
    de LlamaIndex del backend de Django para que genere los embeddings 
    y los guarde en Supabase (vector database).
    """
    url = "http://127.0.0.1:8001/api/llamaindex/indexar/"
    
    texto_conocimiento = f"Profesor: {nombre}. Títulos: {titulos}."
    
    data = {"texto": texto_conocimiento}
    payload = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ctx) as response:
            respuesta = response.read().decode('utf-8')
            print(f"✅ Éxito al indexar a {nombre}")
    except Exception as e:
        print(f"❌ Error al indexar a {nombre}: {e}")

if __name__ == "__main__":
    profesores = [
        {"nombre": "Adolfo Eslava Gómez", "titulos": "Doctor en Estudios Políticos por Universidad Externado de Colombia, Colombia (Ciencias Políticas)"},
        {"nombre": "Adriana Marcela Ramirez Baracaldo", "titulos": "Ph.D. en Procesos Políticos Contemporáneos por Universidad de Salamanca, España (Ciencias Políticas)"},
        {"nombre": "Alba Patricia Cardona Zuluaga", "titulos": "Doctora en Historia por Universidad de los Andes, Colombia (Humanidades / Historia)"},
        {"nombre": "Alberto Ceballos Velásquez", "titulos": "Especialista en Derecho Procesal por Universidad Pontificia Bolivariana, Colombia (Jurisprudencia / Derecho)"},
        {"nombre": "Alejandra María Carmona Duque", "titulos": "Ph.D. en Ingeniería - Recursos Hidráulicos por Universidad Nacional de Colombia, Colombia (Ingeniería / Ciencias Exactas)"},
        {"nombre": "Alejandra María Toro Murillo", "titulos": "Doctora en Estudios hispánicos y latinoamericanos por Universidad de la Sorbona París 3, Francia (Literatura / Estudios Culturales)"},
        {"nombre": "Alejandra María Velásquez Posada", "titulos": "Magíster en Ingeniería, Especialista en Diseño por Universidad EAFIT / UPB, Colombia (Diseño Industrial / Innovación)"},
        {"nombre": "Alejandra Ríos Ramírez", "titulos": "Candidata a Doctora en Ética y Democracia por Universidad de Valencia, España (Filosofía Política / Ética)"}
    ]
    
    print("Iniciando indexación de la lista de profesores en Supabase...\n")
    
    for prof in profesores:
        invocar_ingesta_profesor(prof["nombre"], prof["titulos"])
        # Pausa ligera para no saturar la API gratuita de Gemini
        time.sleep(2)
        
    print("\n¡Proceso de indexación completado!")
