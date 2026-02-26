from django.shortcuts import render

# Create your views here.
from django.http import HtmlResponse

def test_api_connection(request):
    # Datos de prueba preparados para validar la interfaz en inglés o español
    data = {
        "status": "success",
        "message_es": "¡Conexión exitosa entre Angular y Django!",
        "message_en": "Successful connection between Angular and Django!",
        "ui_modules": [
            "campus_and_location",
            "available_classrooms",
            "restaurants",
            "events",
            "academic_calendar",
            "directory",
            "groups_and_seedbeds"
        ]
    }
    return HtmlResponse(data)