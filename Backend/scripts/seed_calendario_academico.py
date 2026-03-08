import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

# Configuración Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

print("Cargando modelo local...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def generar_embedding_local(texto):
    return model.encode(texto).tolist()


# ==========================
# DATOS CALENDARIO ACADÉMICO
# ==========================

datos_calendario = [

{
"actividad": "Formulario de inscripción pregrado",
"descripcion": "Diligenciar el formulario de inscripción para aspirantes a programas de pregrado. Aplica para bachilleres, transferencias externas, reingresos y reintegros que desean ingresar o regresar a la universidad.",
"dirigido_a": "Aspirantes",
"fecha_inicio": "2026-02-24",
"fecha_fin": "2026-06-19",
"periodo": "2026-1",
"meta": {"categoria":"admisiones"}
},

{
"actividad": "Formulario de inscripción pregrado",
"descripcion": "Diligenciar formulario de inscripción para aspirantes a pregrado en procesos de bachilleres, transferencias externas, reintegros o reingresos.",
"dirigido_a": "Aspirantes",
"fecha_inicio": "2026-08-25",
"fecha_fin": "2026-11-20",
"periodo": "2026-2",
"meta": {"categoria":"admisiones"}
},

{
"actividad": "Registro de materias",
"descripcion": "Registro de materias para estudiantes de pregrado a través del sistema académico. Los estudiantes deben seleccionar las asignaturas que cursarán en el semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-05-11",
"fecha_fin": "2026-05-22",
"periodo": "2026-2",
"meta": {"categoria":"matricula"}
},

{
"actividad": "Registro de materias",
"descripcion": "Registro de materias para estudiantes activos en el semestre académico mediante el autoservicio institucional.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-10-26",
"fecha_fin": "2026-11-06",
"periodo": "2027-1",
"meta": {"categoria":"matricula"}
},

{
"actividad": "Solicitud levantamiento de requisitos",
"descripcion": "Solicitudes para cursar materias o realizar práctica levantando prerrequisitos académicos. No aplica para controles de idioma.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-04-27",
"fecha_fin": "2026-07-24",
"periodo": "2026-2",
"meta": {"categoria":"tramites"}
},

{
"actividad": "Solicitud levantamiento de requisitos",
"descripcion": "Solicitud académica para levantar prerrequisitos y poder cursar materias o prácticas durante el semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-10-26",
"fecha_fin": "2027-01-23",
"periodo": "2027-1",
"meta": {"categoria":"tramites"}
},

{
"actividad": "Pago de matrícula estudiantes nuevos",
"descripcion": "Pago de matrícula para estudiantes nuevos, transferencias externas o cupos reservados en programas de pregrado.",
"dirigido_a": "Estudiantes nuevos",
"fecha_inicio": "2026-03-18",
"fecha_fin": "2026-05-27",
"periodo": "2026-2",
"meta": {"categoria":"matricula"}
},

{
"actividad": "Pago de matrícula estudiantes nuevos",
"descripcion": "Pago de matrícula para estudiantes admitidos en programas de pregrado incluyendo transferencias externas.",
"dirigido_a": "Estudiantes nuevos",
"fecha_inicio": "2026-09-16",
"fecha_fin": "2026-11-15",
"periodo": "2027-1",
"meta": {"categoria":"matricula"}
},

{
"actividad": "Inicio de clases",
"descripcion": "Inicio de clases del semestre académico para estudiantes de pregrado.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-01-19",
"fecha_fin": "2026-05-16",
"periodo": "2026-1",
"meta": {"categoria":"clases"}
},

{
"actividad": "Inicio de clases",
"descripcion": "Periodo de clases del segundo semestre académico para estudiantes de pregrado.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-07-21",
"fecha_fin": "2026-11-14",
"periodo": "2026-2",
"meta": {"categoria":"clases"}
},

{
"actividad": "Evaluaciones finales",
"descripcion": "Periodo de evaluaciones finales programadas por los profesores para asignaturas del semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-05-19",
"fecha_fin": "2026-05-30",
"periodo": "2026-1",
"meta": {"categoria":"evaluaciones"}
},

{
"actividad": "Evaluaciones finales",
"descripcion": "Periodo de exámenes finales de asignaturas programadas por los profesores.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-11-17",
"fecha_fin": "2026-11-28",
"periodo": "2026-2",
"meta": {"categoria":"evaluaciones"}
}

]


# ==========================
# INSERTAR EN SUPABASE
# ==========================

for item in datos_calendario:

    print(f"Procesando actividad: {item['actividad']}")

    texto_embedding = f"""
    Actividad: {item['actividad']}
    Descripción: {item['descripcion']}
    Dirigido a: {item['dirigido_a']}
    Fecha inicio: {item['fecha_inicio']}
    Fecha fin: {item['fecha_fin']}
    Periodo académico: {item['periodo']}
    """

    vector = generar_embedding_local(texto_embedding)

    supabase.table("calendario_academico").insert({
        "actividad": item["actividad"],
        "descripcion": item["descripcion"],
        "dirigido_a": item["dirigido_a"],
        "fecha_inicio": item["fecha_inicio"],
        "fecha_fin": item["fecha_fin"],
        "periodo": item["periodo"],
        "embedding": vector
    }).execute()

print("Dataset del calendario académico cargado correctamente")