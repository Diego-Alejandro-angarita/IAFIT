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
# Cada evento tiene un campo 'embedding_text' con lenguaje natural rico
# que anticipa las preguntas del usuario para mejorar la búsqueda semántica.

datos_calendario = [

{
"actividad": "Formulario de inscripción pregrado",
"descripcion": "Diligenciar el formulario de inscripción para aspirantes a programas de pregrado. Aplica para bachilleres, transferencias externas, reingresos y reintegros que desean ingresar o regresar a la universidad.",
"dirigido_a": "Aspirantes",
"fecha_inicio": "2026-02-24",
"fecha_fin": "2026-06-19",
"periodo": "2026-1",
"embedding_text": "Inscripción a la universidad primer semestre 2026. ¿Hasta cuándo puedo inscribirme? ¿Cuándo abren inscripciones? Formulario de inscripción pregrado para aspirantes, bachilleres, transferencias externas, reingresos y reintegros. Las inscripciones están abiertas del 24 de febrero al 19 de junio de 2026 para el periodo 2026-1. Fecha límite de inscripción primer semestre. Proceso de admisión. ¿Cómo me inscribo en la universidad?"
},

{
"actividad": "Formulario de inscripción pregrado",
"descripcion": "Diligenciar formulario de inscripción para aspirantes a pregrado en procesos de bachilleres, transferencias externas, reintegros o reingresos.",
"dirigido_a": "Aspirantes",
"fecha_inicio": "2026-08-25",
"fecha_fin": "2026-11-20",
"periodo": "2026-2",
"embedding_text": "Inscripción a la universidad segundo semestre 2026. Formulario de inscripción pregrado para aspirantes, bachilleres, transferencias externas, reingresos y reintegros. Las inscripciones del segundo semestre están abiertas del 25 de agosto al 20 de noviembre de 2026 para el periodo 2026-2. Fecha límite inscripción segundo semestre. Admisión segundo periodo."
},

{
"actividad": "Registro de materias",
"descripcion": "Registro de materias para estudiantes de pregrado a través del sistema académico. Los estudiantes deben seleccionar las asignaturas que cursarán en el semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-05-11",
"fecha_fin": "2026-05-22",
"periodo": "2026-2",
"embedding_text": "Registro y selección de materias segundo semestre 2026. ¿Cuándo puedo registrar materias? ¿Cuándo es el registro de asignaturas? Matrícula académica de materias. Los estudiantes activos pueden registrar sus materias del 11 al 22 de mayo de 2026 para el periodo 2026-2. Selección de asignaturas. Inscripción de cursos del semestre."
},

{
"actividad": "Registro de materias",
"descripcion": "Registro de materias para estudiantes activos en el semestre académico mediante el autoservicio institucional.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-10-26",
"fecha_fin": "2026-11-06",
"periodo": "2027-1",
"embedding_text": "Registro y selección de materias primer semestre 2027. Matrícula académica de materias. Los estudiantes activos pueden registrar sus materias del 26 de octubre al 6 de noviembre de 2026 para el periodo 2027-1. Selección de asignaturas para el siguiente semestre. ¿Cuándo registro materias del próximo semestre?"
},

{
"actividad": "Solicitud levantamiento de requisitos",
"descripcion": "Solicitudes para cursar materias o realizar práctica levantando prerrequisitos académicos. No aplica para controles de idioma.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-04-27",
"fecha_fin": "2026-07-24",
"periodo": "2026-2",
"embedding_text": "Levantamiento de prerrequisitos segundo semestre 2026. ¿Cómo levanto un prerrequisito? ¿Cuándo puedo solicitar levantamiento de requisitos? Solicitud para cursar materias sin haber aprobado el prerrequisito. Disponible del 27 de abril al 24 de julio de 2026 para periodo 2026-2. No aplica para idiomas."
},

{
"actividad": "Solicitud levantamiento de requisitos",
"descripcion": "Solicitud académica para levantar prerrequisitos y poder cursar materias o prácticas durante el semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-10-26",
"fecha_fin": "2027-01-23",
"periodo": "2027-1",
"embedding_text": "Levantamiento de prerrequisitos primer semestre 2027. Solicitud para cursar materias o prácticas sin prerrequisito aprobado. Disponible del 26 de octubre de 2026 al 23 de enero de 2027 para periodo 2027-1. Levantar requisitos académicos."
},

{
"actividad": "Pago de matrícula estudiantes nuevos",
"descripcion": "Pago de matrícula para estudiantes nuevos, transferencias externas o cupos reservados en programas de pregrado.",
"dirigido_a": "Estudiantes nuevos",
"fecha_inicio": "2026-03-18",
"fecha_fin": "2026-05-27",
"periodo": "2026-2",
"embedding_text": "Pago de matrícula para estudiantes nuevos segundo semestre 2026. ¿Cuándo debo pagar la matrícula? ¿Hasta cuándo puedo pagar? Fecha límite de pago matrícula nuevos. Estudiantes nuevos, transferencias externas y cupos reservados deben pagar del 18 de marzo al 27 de mayo de 2026 para el periodo 2026-2. Cuánto cuesta la matrícula. Valor matrícula pregrado."
},

{
"actividad": "Pago de matrícula estudiantes nuevos",
"descripcion": "Pago de matrícula para estudiantes admitidos en programas de pregrado incluyendo transferencias externas.",
"dirigido_a": "Estudiantes nuevos",
"fecha_inicio": "2026-09-16",
"fecha_fin": "2026-11-15",
"periodo": "2027-1",
"embedding_text": "Pago de matrícula para estudiantes nuevos primer semestre 2027. Fecha límite de pago matrícula admitidos. Estudiantes nuevos y transferencias externas deben pagar del 16 de septiembre al 15 de noviembre de 2026 para el periodo 2027-1. ¿Cuándo pago la matrícula del próximo semestre?"
},

{
"actividad": "Inicio de clases",
"descripcion": "Periodo de clases del primer semestre académico para estudiantes de pregrado. Las clases van del 19 de enero al 16 de mayo de 2026.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-01-19",
"fecha_fin": "2026-05-16",
"periodo": "2026-1",
"embedding_text": "Inicio y fin de clases primer semestre 2026. ¿Cuándo empiezan las clases? ¿Cuándo se acaban las clases del primer semestre? Las clases del primer semestre 2026 van del 19 de enero al 16 de mayo de 2026. Periodo académico 2026-1. ¿Cuándo terminan las clases? Último día de clases primer semestre es el 16 de mayo."
},

{
"actividad": "Inicio de clases",
"descripcion": "Periodo de clases del segundo semestre académico para estudiantes de pregrado. Las clases van del 21 de julio al 14 de noviembre de 2026.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-07-21",
"fecha_fin": "2026-11-14",
"periodo": "2026-2",
"embedding_text": "Inicio y fin de clases segundo semestre 2026. ¿Cuándo empiezan las clases del segundo semestre? ¿Cuándo se acaban las clases? Las clases del segundo semestre 2026 van del 21 de julio al 14 de noviembre de 2026. Periodo académico 2026-2. ¿Cuándo terminan las clases? Último día de clases segundo semestre es el 14 de noviembre."
},

{
"actividad": "Evaluaciones finales",
"descripcion": "Periodo de evaluaciones finales programadas por los profesores para asignaturas del primer semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-05-19",
"fecha_fin": "2026-05-30",
"periodo": "2026-1",
"embedding_text": "Exámenes finales primer semestre 2026. ¿Cuándo son los parciales finales? ¿Cuándo son las evaluaciones finales del primer semestre? Los exámenes finales del periodo 2026-1 son del 19 al 30 de mayo de 2026. Periodo de finales. Semana de finales primer semestre. ¿Cuándo presento los finales?"
},

{
"actividad": "Evaluaciones finales",
"descripcion": "Periodo de exámenes finales de asignaturas programadas por los profesores del segundo semestre.",
"dirigido_a": "Estudiantes activos",
"fecha_inicio": "2026-11-17",
"fecha_fin": "2026-11-28",
"periodo": "2026-2",
"embedding_text": "Exámenes finales segundo semestre 2026. ¿Cuándo son las evaluaciones finales del segundo semestre? Los exámenes finales del periodo 2026-2 son del 17 al 28 de noviembre de 2026. Periodo de finales segundo semestre. Semana de finales. ¿Cuándo presento los finales del segundo semestre?"
}

]


# ==========================
# LIMPIAR DATOS EXISTENTES
# ==========================
print("Eliminando datos existentes del calendario...")
supabase.table("calendario_academico").delete().neq("actividad", "").execute()
print("Datos anteriores eliminados.")


# ==========================
# INSERTAR EN SUPABASE
# ==========================

for item in datos_calendario:

    print(f"Procesando actividad: {item['actividad']} ({item['periodo']})")

    vector = generar_embedding_local(item["embedding_text"])

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