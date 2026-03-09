import os
import json
import uuid
import asgiref
from dotenv import load_dotenv
from llama_index.embeddings.gemini import GeminiEmbedding

load_dotenv()

embed_model = GeminiEmbedding(api_key=os.environ['GEMINI_API_KEY'], model_name='models/gemini-embedding-001')

data = [
    "Profesor: Adolfo Eslava Gómez. Títulos: Doctor en Estudios Políticos por Universidad Externado de Colombia, Colombia (Ciencias Políticas).",
    "Profesor: Adriana Marcela Ramirez Baracaldo. Títulos: Ph.D. en Procesos Políticos Contemporáneos por Universidad de Salamanca, España (Ciencias Políticas).",
    "Profesor: Alba Patricia Cardona Zuluaga. Títulos: Doctora en Historia por Universidad de los Andes, Colombia (Humanidades / Historia).",
    "Profesor: Alberto Ceballos Velásquez. Títulos: Especialista en Derecho Procesal por Universidad Pontificia Bolivariana, Colombia (Jurisprudencia / Derecho).",
    "Profesor: Alejandra María Carmona Duque. Títulos: Ph.D. en Ingeniería - Recursos Hidráulicos por Universidad Nacional de Colombia, Colombia (Ingeniería / Ciencias Exactas).",
    "Profesor: Alejandra María Toro Murillo. Títulos: Doctora en Estudios hispánicos y latinoamericanos por Universidad de la Sorbona París 3, Francia (Literatura / Estudios Culturales).",
    "Profesor: Alejandra María Velásquez Posada. Títulos: Magíster en Ingeniería, Especialista en Diseño por Universidad EAFIT / UPB, Colombia (Diseño Industrial / Innovación).",
    "Profesor: Alejandra Ríos Ramírez. Títulos: Candidata a Doctora en Ética y Democracia por Universidad de Valencia, España (Filosofía Política / Ética)."
]

sql = "INSERT INTO data_eafit_knowledge (id, node_id, text, metadata_, embedding) VALUES\n"
values = []

for text in data:
    emb = embed_model.get_text_embedding(text)
    node_id = str(uuid.uuid4())
    
    # LlamaIndex expects a specific metadata structure for its nodes
    meta_dict = {
        "_node_type": "TextNode",
        "_node_content": json.dumps({
            "id_": node_id,
            "embedding": None,
            "metadata": {},
            "excluded_embed_metadata_keys": [],
            "excluded_llm_metadata_keys": [],
            "relationships": {},
            "text": "",
            "start_char_idx": None,
            "end_char_idx": None,
            "text_template": "{metadata_str}\\n\\n{content}",
            "metadata_template": "{key}: {value}",
            "metadata_seperator": "\\n",
            "class_name": "TextNode"
        })
    }
    
    meta_json = json.dumps(meta_dict).replace("'", "''") # Escape single quotes for SQL
    text_escaped = text.replace("'", "''")
    emb_str = f"'[{','.join(map(str, emb))}]'"
    
    values.append(f"(gen_random_uuid(), '{node_id}', '{text_escaped}', '{meta_json}'::jsonb, {emb_str})")

sql += ",\n".join(values) + ";"

with open('profesores_insert.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print("SQL generado exitosamente en profesores_insert.sql")
