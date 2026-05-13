import json
import os
import re
import unicodedata
import uuid
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv
from llama_index.embeddings.gemini import GeminiEmbedding


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


PROFESSORS = [
    {
        "nombre": "Camila Andrea Restrepo Mesa",
        "titulos": "Magister en Analitica de Datos por Universidad EAFIT, Colombia (Ciencias de Datos / Inteligencia Artificial)",
    },
    {
        "nombre": "Daniel Felipe Moreno Ruiz",
        "titulos": "Doctor en Ingenieria de Sistemas por Universidad Nacional de Colombia, Colombia (Ingenieria / Software)",
    },
    {
        "nombre": "Laura Sofia Mejia Arango",
        "titulos": "Magister en Diseno de Experiencia de Usuario por Universidad EAFIT, Colombia (Diseno / Innovacion Digital)",
    },
    {
        "nombre": "Mateo Alejandro Giraldo Perez",
        "titulos": "Doctor en Economia Aplicada por Universidad de los Andes, Colombia (Economia / Politica Publica)",
    },
    {
        "nombre": "Valentina Isabel Torres Cano",
        "titulos": "Magister en Administracion por Universidad EAFIT, Colombia (Administracion / Estrategia)",
    },
    {
        "nombre": "Santiago Andres Ospina Lopez",
        "titulos": "Doctor en Matematicas Aplicadas por Universidad de Antioquia, Colombia (Matematicas / Modelacion)",
    },
    {
        "nombre": "Natalia Fernanda Cardenas Rios",
        "titulos": "Magister en Comunicacion Transmedia por Universidad EAFIT, Colombia (Comunicacion / Medios Digitales)",
    },
    {
        "nombre": "Juan David Salazar Gomez",
        "titulos": "Doctor en Derecho por Universidad Externado de Colombia, Colombia (Derecho / Derecho Publico)",
    },
    {
        "nombre": "Mariana Lucia Alvarez Botero",
        "titulos": "Magister en Finanzas por Universidad EAFIT, Colombia (Finanzas / Riesgo)",
    },
    {
        "nombre": "Sebastian Nicolas Herrera Vargas",
        "titulos": "Doctor en Ciencias de la Computacion por Universidad Politecnica de Madrid, Espana (Computacion / IA)",
    },
    {
        "nombre": "Isabella Maria Zapata Correa",
        "titulos": "Magister en Estudios Humanisticos por Universidad EAFIT, Colombia (Humanidades / Cultura)",
    },
    {
        "nombre": "Tomas Eduardo Ramirez Villegas",
        "titulos": "Doctor en Ingenieria Civil por Universidad Nacional de Colombia, Colombia (Ingenieria / Infraestructura)",
    },
]


def normalize_token(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]", "", ascii_value).lower()


def build_email(nombre: str) -> str:
    parts = [normalize_token(part) for part in nombre.split() if normalize_token(part)]
    if not parts:
        raise ValueError("El nombre no tiene tokens validos")
    first = parts[0][:2]
    second = parts[1] if len(parts) > 1 else parts[0]
    return f"{first}{second}@eafit.edu.do"


def parse_name(text: str) -> str | None:
    match = re.search(r"Profesor:\s*(.*?)\.\s*T[íi]tulos:", text)
    if match:
        return match.group(1).strip()
    return None


def node_metadata(node_id: str) -> dict:
    return {
        "_node_type": "TextNode",
        "_node_content": json.dumps(
            {
                "id_": node_id,
                "embedding": None,
                "metadata": {},
                "excluded_embed_metadata_keys": [],
                "excluded_llm_metadata_keys": [],
                "relationships": {},
                "text": "",
                "start_char_idx": None,
                "end_char_idx": None,
                "text_template": "{metadata_str}\n\n{content}",
                "metadata_template": "{key}: {value}",
                "metadata_seperator": "\n",
                "class_name": "TextNode",
            }
        ),
    }


def main() -> None:
    db_url = os.environ.get("SUPABASE_DB_URL")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not db_url:
        raise RuntimeError("SUPABASE_DB_URL no esta configurado en Backend/.env")
    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY no esta configurado en Backend/.env")

    parsed = urlparse(db_url)
    embed_model = GeminiEmbedding(api_key=gemini_key, model_name="models/gemini-embedding-001")

    conn = psycopg2.connect(
        dbname=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port or 5432,
        sslmode="require",
    )

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("ALTER TABLE data_info_directorio ADD COLUMN IF NOT EXISTS email text;")

                cur.execute("SELECT id, text FROM data_info_directorio WHERE email IS NULL OR email = '';")
                updated = 0
                for row_id, text in cur.fetchall():
                    nombre = parse_name(text or "")
                    if not nombre:
                        continue
                    cur.execute(
                        "UPDATE data_info_directorio SET email = %s WHERE id = %s;",
                        (build_email(nombre), row_id),
                    )
                    updated += 1

                inserted = 0
                for professor in PROFESSORS:
                    nombre = professor["nombre"]
                    titulos = professor["titulos"]
                    email = build_email(nombre)
                    text = f"Profesor: {nombre}. Títulos: {titulos}."

                    cur.execute(
                        "SELECT 1 FROM data_info_directorio WHERE text = %s OR email = %s LIMIT 1;",
                        (text, email),
                    )
                    if cur.fetchone():
                        continue

                    node_id = str(uuid.uuid4())
                    embedding = embed_model.get_text_embedding(text)
                    cur.execute(
                        """
                        INSERT INTO data_info_directorio (node_id, text, metadata_, embedding, email)
                        VALUES (%s, %s, %s::jsonb, %s, %s);
                        """,
                        (
                            node_id,
                            text,
                            json.dumps(node_metadata(node_id)),
                            f"[{','.join(map(str, embedding))}]",
                            email,
                        ),
                    )
                    inserted += 1

                cur.execute("SELECT count(*), count(email) FROM data_info_directorio;")
                total_rows, rows_with_email = cur.fetchone()
                cur.execute(
                    """
                    SELECT email
                    FROM data_info_directorio
                    WHERE email IS NOT NULL AND email <> ''
                    ORDER BY id DESC
                    LIMIT 5;
                    """
                )
                sample_emails = [row[0] for row in cur.fetchall()]

        print(f"Columna email lista. Emails actualizados: {updated}. Profesores nuevos insertados: {inserted}.")
        print(f"Filas totales: {total_rows}. Filas con email: {rows_with_email}.")
        print(f"Muestra de emails: {', '.join(sample_emails)}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
