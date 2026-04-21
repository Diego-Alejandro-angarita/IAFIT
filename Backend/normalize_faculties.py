"""
Script para normalizar los nombres de facultades en la tabla Seedbed.
Elimina espacios unicode invisibles y consolida nombres similares.
"""
import os
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from research.models import Seedbed

# Mapeo de normalización de facultades
FACULTY_MAPPING = {
    # Consolidar variantes a nombres estándar
    'Escuela de Ciencias Aplicadas e Ingeniería': 'Ciencias Aplicadas e Ingeniería',
    'Escuela de Derecho': 'Derecho',
    'Escuela de Administración': 'Administración',
    'Escuela de Artes y Humanidades': 'Artes y Humanidades',
    'Escuelas de Artes y Humanidades': 'Artes y Humanidades',
    'Escuela de Finanzas, Economía y Gobierno': 'Finanzas, Economía y Gobierno',
    
    # Especialidades a sus escuelas principales
    'Ingeniería de Diseño de Producto': 'Ciencias Aplicadas e Ingeniería',
    'Ingeniería Mecánica': 'Ciencias Aplicadas e Ingeniería',
    'Ingeniería de Sistemas': 'Ciencias Aplicadas e Ingeniería',
    'Ingeniería Civil': 'Ciencias Aplicadas e Ingeniería',
    'Ingeniería de Producción': 'Ciencias Aplicadas e Ingeniería',
    'Ingenieria Agronómica': 'Ciencias Aplicadas e Ingeniería',
    'Ciencias Biológicas': 'Ciencias Aplicadas e Ingeniería',
    'Ciencias Físicas': 'Ciencias Aplicadas e Ingeniería',
    'Ciencias de la Tierra': 'Ciencias Aplicadas e Ingeniería',
    
    'Comunicación social': 'Artes y Humanidades',
    'Comunicación Social': 'Artes y Humanidades',
    'Música': 'Artes y Humanidades',
    'Humanidades': 'Artes y Humanidades',
    'Diseño Interactivo': 'Artes y Humanidades',
    'Psicología': 'Artes y Humanidades',
    
    'Mercadeo': 'Administración',
    'Negocios Internacionales': 'Administración',
    
    'Economía': 'Finanzas, Economía y Gobierno',
    
    # Datos de prueba/basura
    'Tooltip prueba': 'Unknown',
}

def clean_unicode_spaces(text):
    """Elimina espacios unicode invisibles y normaliza espacios."""
    # Reemplaza varios tipos de espacios unicode con espacio normal
    text = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff\u00a0\u2002\u2003\u2009\u200a]+', '', text)
    # Elimina espacios al inicio y final
    text = text.strip()
    # Normaliza múltiples espacios a uno solo
    text = re.sub(r'\s+', ' ', text)
    return text

def normalize_faculty():
    seedbeds = Seedbed.objects.all()
    updated = 0
    
    print("Normalizando facultades...")
    print("-" * 60)
    
    for seedbed in seedbeds:
        original = seedbed.faculty
        
        # Paso 1: Limpiar espacios unicode
        cleaned = clean_unicode_spaces(original)
        
        # Paso 2: Aplicar mapeo si existe
        final = FACULTY_MAPPING.get(cleaned, cleaned)
        
        # Si cambió, actualizar
        if final != original:
            print(f"'{original}' -> '{final}' ({seedbed.name[:50]}...)")
            seedbed.faculty = final
            seedbed.save()
            updated += 1
    
    print("-" * 60)
    print(f"Total actualizados: {updated}")
    
    # Mostrar resumen final
    print("\nResumen de facultades después de normalización:")
    from django.db.models import Count
    faculties = Seedbed.objects.values('faculty').annotate(total=Count('id')).order_by('-total')
    for f in faculties:
        print(f"  {f['faculty']}: {f['total']}")

if __name__ == '__main__':
    normalize_faculty()
