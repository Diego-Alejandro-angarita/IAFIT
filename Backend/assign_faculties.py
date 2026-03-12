"""
Script para asignar facultades a semilleros con 'Unknown'.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from research.models import Seedbed

# Mapeo de semilleros específicos a sus facultades
SEEDBED_FACULTY_MAPPING = {
    'Semillero de Investigación Contable (SEIC)': 'Administración',
    'Semillero de Investigación DATAPOL': 'Finanzas, Economía y Gobierno',
    'Semillero de Investigación en Control, Auditoría y Administración de Riesgos (SICAR)': 'Administración',
    'Semillero de Investigación en Estrategia (SIE)': 'Administración',
    'Semillero de Investigación en Gestión Humana Organizacional SIGHO': 'Administración',
    'Semillero de Investigación en Innovación y Emprendimiento (SIIE)': 'Administración',
    'Semillero de Investigación en Mejoramiento de Procesos (SIMPRO)': 'Administración',
    'Semillero de Investigación en Mercadeo (SMART)': 'Administración',
    'Semillero de Investigación en Musicología Histórica (SIMUH)': 'Artes y Humanidades',
    'Semillero de Investigación en Prácticas y Redes Empresariales (SIPRE)': 'Administración',
    'Semillero de Investigación Observatorio en Comercio, Inversión y Desarrollo': 'Finanzas, Economía y Gobierno',
}

def assign_faculties():
    updated = 0
    
    print("Asignando facultades a semilleros con 'Unknown'...")
    print("-" * 60)
    
    for name, faculty in SEEDBED_FACULTY_MAPPING.items():
        try:
            seedbed = Seedbed.objects.get(name=name)
            if seedbed.faculty == 'Unknown':
                print(f"'{name}' -> '{faculty}'")
                seedbed.faculty = faculty
                seedbed.save()
                updated += 1
            else:
                print(f"'{name}' ya tiene facultad: {seedbed.faculty}")
        except Seedbed.DoesNotExist:
            print(f"No encontrado: {name}")
    
    print("-" * 60)
    print(f"Total actualizados: {updated}")
    
    # Mostrar resumen final
    print("\nResumen de facultades después de asignación:")
    from django.db.models import Count
    faculties = Seedbed.objects.values('faculty').annotate(total=Count('id')).order_by('-total')
    for f in faculties:
        print(f"  {f['faculty']}: {f['total']}")

if __name__ == '__main__':
    assign_faculties()
