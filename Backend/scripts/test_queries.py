"""Quick test script for calendar search queries."""
import urllib.request
import json

BASE = "http://127.0.0.1:8001/api/llamaindex/calendario/buscar/"

queries = [
    "hasta cuando puedo inscribirme a la universidad",
    "cuando se acaban las clases",
    "cuando son los examenes finales",
    "cuando puedo registrar materias",
    "cuando debo pagar la matricula",
    "cuando empiezan las clases del segundo semestre",
]

for q in queries:
    print(f"\n{'='*60}")
    print(f"PREGUNTA: {q}")
    print(f"{'='*60}")
    url = BASE + "?q=" + urllib.parse.quote(q)
    try:
        r = urllib.request.urlopen(url)
        d = json.loads(r.read())
        for e in d["resultados"]:
            print(f"  {e['actividad']} | {e['periodo']} | {e['fecha_inicio']} - {e['fecha_fin']} | sim={e['similitud']:.3f}")
        if not d["resultados"]:
            print("  (sin resultados)")
    except Exception as ex:
        print(f"  ERROR: {ex}")
