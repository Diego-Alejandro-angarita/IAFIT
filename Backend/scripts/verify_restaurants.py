import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=" * 80)
print("VERIFICACIÓN DE DATOS EN LA TABLA 'restaurants'")
print("=" * 80)

with connection.cursor() as cursor:
    # Obtener información de la tabla
    cursor.execute("""
        SELECT 
            restaurant_name, 
            location, 
            schedule,
            contact_info
        FROM restaurants 
        ORDER BY restaurant_name;
    """)
    
    restaurants = cursor.fetchall()
    
    print(f"\n✓ Total de restaurantes: {len(restaurants)}\n")
    
    for i, (name, location, schedule, contact) in enumerate(restaurants, 1):
        print(f"{i:2}. {name}")
        print(f"    📍 {location}")
        print(f"    🕒 {schedule}")
        print(f"    📞 {contact}")
        print()

print("=" * 80)
