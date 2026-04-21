#!/usr/bin/env python
"""
Script to migrate 17 EAFIT restaurants to Django Establishment model
Uses correct field names
"""

import os
import sys
import django
from datetime import time

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LlamaIndex.models import Establishment, Category, EstablishmentCategory, Schedule

print("\n" + "="*80)
print("MIGRANDO RESTAURANTES A MODELOS DE DJANGO")
print("="*80 + "\n")

# Define the 17 restaurants with correct field names
restaurants_data = [
    {
        "name": "Bigo's",
        "location": "EAFIT",
        "description": "Restaurante de comida rápida",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "comida_rapida",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Coffee House",
        "location": "EAFIT",
        "description": "Café especializado",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "De Lolita",
        "location": "EAFIT",
        "description": "Restaurante internacional",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["internacional"]
    },
    {
        "name": "Dogger",
        "location": "EAFIT",
        "description": "Comida rápida - hamburguesas",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "comida_rapida",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Dunkin Donuts",
        "location": "EAFIT",
        "description": "Café y donuts",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "El Tejadito",
        "location": "EAFIT",
        "description": "Comida típica colombiana",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["almuerzo"]
    },
    {
        "name": "Frisby",
        "location": "EAFIT",
        "description": "Pollo frito y comida rápida",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "comida_rapida",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Home Food",
        "location": "EAFIT",
        "description": "Comida casera",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["almuerzo"]
    },
    {
        "name": "Juan Valdez Café",
        "location": "EAFIT",
        "description": "Café premium",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "La Cafetería",
        "location": "EAFIT",
        "description": "Café y desayunos",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "Madelo",
        "location": "EAFIT",
        "description": "Restaurante internacional",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["internacional"]
    },
    {
        "name": "Mi buñuelo",
        "location": "EAFIT",
        "description": "Comida típica y postres",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "snack",
        "categories": ["postres"]
    },
    {
        "name": "Pimientos",
        "location": "EAFIT",
        "description": "Comida saludable",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["saludable"]
    },
    {
        "name": "Plural",
        "location": "EAFIT",
        "description": "Restaurante diverso",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["almuerzo"]
    },
    {
        "name": "Subway",
        "location": "EAFIT",
        "description": "Sándwiches frescos",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "comida_rapida",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Taco Factory",
        "location": "EAFIT",
        "description": "Comida mexicana",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "comida_rapida",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Aldea Nikkei",
        "location": "EAFIT",
        "description": "Comida asiática",
        "phone": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurante",
        "categories": ["internacional"]
    }
]

try:
    # Step 1: Clear existing data
    print("1. Limpiando datos existentes...")
    Establishment.objects.all().delete()
    print("   ✓ Establecimientos eliminados")
    
    # Step 2: Create categories
    print("\n2. Creando categorías...")
    category_mapping = {
        'almuerzo': 'almuerzo',
        'cafe': 'cafe',
        'vegetariano': 'vegetariano',
        'postres': 'postres',
        'bebidas': 'bebidas',
        'comida_rapida': 'comida_rapida',
        'internacional': 'internacional',
        'saludable': 'saludable'
    }
    
    categories = {}
    for cat_key, cat_value in category_mapping.items():
        try:
            cat, created = Category.objects.get_or_create(
                name=cat_key,
                defaults={'description': f'Categoría: {cat_key}'}
            )
            categories[cat_key] = cat
            status = "creada" if created else "existente"
            print(f"   ✓ {cat.get_name_display()} ({status})")
        except Exception as e:
            print(f"   ✗ Error creando {cat_key}: {e}")
    
    # Step 3: Create establishments
    print("\n3. Creando establecimientos...")
    establishments = {}
    for i, rest_data in enumerate(restaurants_data, 1):
        try:
            est = Establishment.objects.create(
                name=rest_data["name"],
                description=rest_data["description"],
                location=rest_data["location"],
                phone=rest_data["phone"],
                establishment_type=rest_data["establishment_type"]
            )
            establishments[rest_data["name"]] = est
            print(f"   ✓ {i}. {rest_data['name']}")
        except Exception as e:
            print(f"   ✗ Error creando {rest_data['name']}: {e}")
    
    # Step 4: Assign categories
    print("\n4. Asignando categorías...")
    for rest_data in restaurants_data:
        try:
            est = establishments.get(rest_data["name"])
            if est:
                for cat_key in rest_data["categories"]:
                    if cat_key in categories:
                        EstablishmentCategory.objects.get_or_create(
                            establishment=est,
                            category=categories[cat_key]
                        )
                print(f"   ✓ Categorías asignadas a {rest_data['name']}")
        except Exception as e:
            print(f"   ✗ Error asignando categorías a {rest_data['name']}: {e}")
    
    # Step 5: Create schedules (7 days, same hours for all)
    print("\n5. Creando horarios...")
    opening_time = time(6, 30)  # 6:30 AM
    closing_time = time(20, 0)   # 8:00 PM
    
    for est_name, est in establishments.items():
        try:
            for day_num in range(1, 8):  # 1=Monday, 7=Sunday
                Schedule.objects.get_or_create(
                    establishment=est,
                    day_of_week=day_num,
                    defaults={
                        'opening_time': opening_time,
                        'closing_time': closing_time,
                        'is_open': True
                    }
                )
            print(f"   ✓ Horarios creados para {est_name}")
        except Exception as e:
            print(f"   ✗ Error creando horarios para {est_name}: {e}")
    
    # Verification
    print("\n" + "="*80)
    print("VERIFICACIÓN")
    print("="*80)
    total_ests = Establishment.objects.count()
    total_cats = Category.objects.count()
    print(f"\n✓ Total de establecimientos: {total_ests}")
    print(f"✓ Total de categorías: {total_cats}")
    
    print("\nEstablecimientos creados:")
    for est in Establishment.objects.all().order_by('name'):
        cats = est.categories.all()
        cat_names = ", ".join([cat.get_name_display() for cat in cats]) if cats.exists() else "Sin categorías"
        print(f"  • {est.name} - {cat_names}")
    
    print("\n" + "="*80)
    if total_ests == 17:
        print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE - 17 RESTAURANTES CREADOS")
    else:
        print(f"⚠ MIGRACIÓN COMPLETADA - Solo {total_ests} restaurantes (se esperaban 17)")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR DURANTE LA MIGRACIÓN: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
