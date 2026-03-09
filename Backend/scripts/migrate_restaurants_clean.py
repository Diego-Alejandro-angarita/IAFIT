#!/usr/bin/env python
"""
Script to migrate 17 EAFIT restaurants to Django Establishment model
Simplified version with better error handling
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
print("MIGRANDO RESTAURANTES A MODELOS DE DJANGO (VERSIÓN LIMPIA)")
print("="*80 + "\n")

# Define the 17 restaurants
restaurants_data = [
    {
        "name": "Bigo's",
        "location": "EAFIT",
        "description": "Restaurante de comida rápida",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Coffee House",
        "location": "EAFIT",
        "description": "Café especializado",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "De Lolita",
        "location": "EAFIT",
        "description": "Restaurante internacional",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["internacional"]
    },
    {
        "name": "Dogger",
        "location": "EAFIT",
        "description": "Comida rápida - hamburguesas",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Dunkin Donuts",
        "location": "EAFIT",
        "description": "Café y donuts",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "El Tejadito",
        "location": "EAFIT",
        "description": "Comida típica colombiana",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["almuerzo"]
    },
    {
        "name": "Frisby",
        "location": "EAFIT",
        "description": "Pollo frito y comida rápida",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Home Food",
        "location": "EAFIT",
        "description": "Comida casera",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["almuerzo"]
    },
    {
        "name": "Juan Valdez Café",
        "location": "EAFIT",
        "description": "Café premium",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "La Cafetería",
        "location": "EAFIT",
        "description": "Café y desayunos",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["cafe"]
    },
    {
        "name": "Madelo",
        "location": "EAFIT",
        "description": "Restaurante internacional",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["internacional"]
    },
    {
        "name": "Mi buñuelo",
        "location": "EAFIT",
        "description": "Comida típica y postres",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["postres"]
    },
    {
        "name": "Pimientos",
        "location": "EAFIT",
        "description": "Comida saludable",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["saludable"]
    },
    {
        "name": "Plural",
        "location": "EAFIT",
        "description": "Restaurante diverso",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["almuerzo"]
    },
    {
        "name": "Subway",
        "location": "EAFIT",
        "description": "Sándwiches frescos",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Taco Factory",
        "location": "EAFIT",
        "description": "Comida mexicana",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "cafeteria",
        "categories": ["comida_rapida"]
    },
    {
        "name": "Aldea Nikkei",
        "location": "EAFIT",
        "description": "Comida asiática",
        "contact_info": "+57 4 XXXX-XXXX",
        "establishment_type": "restaurant",
        "categories": ["internacional"]
    }
]

try:
    # Step 1: Clear existing data (catch if tables don't exist)
    print("1. Limpiando datos existentes...")
    try:
        Establishment.objects.all().delete()
        print("   ✓ Establecimientos eliminados")
    except Exception as e:
        print(f"   ⚠ No se pudieron eliminar establecimientos (tabla podría no existir): {e}")
    
    try:
        Category.objects.all().delete()
        print("   ✓ Categorías eliminadas")
    except Exception as e:
        print(f"   ⚠ No se pudieron eliminar categorías (tabla podría no existir): {e}")
    
    # Step 2: Create categories
    print("\n2. Creando categorías...")
    category_choices = {
        'almuerzo': 'Almuerzo',
        'cafe': 'Café',
        'vegetariano': 'Vegetariano',
        'postres': 'Postres',
        'bebidas': 'Bebidas',
        'comida_rapida': 'Comida Rápida',
        'internacional': 'Internacional',
        'saludable': 'Saludable'
    }
    
    categories = {}
    for cat_key, cat_name in category_choices.items():
        try:
            cat, created = Category.objects.get_or_create(category_name=cat_name, defaults={'category_name': cat_name})
            categories[cat_key] = cat
            status = "creada" if created else "existente"
            print(f"   ✓ {cat_name} ({status})")
        except Exception as e:
            print(f"   ✗ Error creando {cat_name}: {e}")
    
    # Step 3: Create establishments
    print("\n3. Creando establecimientos...")
    establishments = {}
    for i, rest_data in enumerate(restaurants_data, 1):
        try:
            est = Establishment.objects.create(
                restaurant_name=rest_data["name"],
                description=rest_data["description"],
                location=rest_data["location"],
                contact_info=rest_data["contact_info"],
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
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    opening_time = time(6, 30)  # 6:30 AM
    closing_time = time(20, 0)   # 8:00 PM
    
    for est_name, est in establishments.items():
        try:
            for day in days:
                Schedule.objects.get_or_create(
                    establishment=est,
                    day_of_week=day,
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
    for est in Establishment.objects.all():
        cats = est.establishmentcategory_set.all()
        cat_names = ", ".join([ec.category.category_name for ec in cats]) if cats.exists() else "Sin categorías"
        print(f"  • {est.restaurant_name} - {cat_names}")
    
    print("\n" + "="*80)
    print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR DURANTE LA MIGRACIÓN: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
