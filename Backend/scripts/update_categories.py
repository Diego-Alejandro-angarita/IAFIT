#!/usr/bin/env python
"""
Script para actualizar las categorías a solo:
- Almuerzos
- Postres
- Desayunos
- Snacks
- Café
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LlamaIndex.models import Establishment, Category, EstablishmentCategory

print("\n" + "="*80)
print("ACTUALIZANDO CATEGORÍAS")
print("="*80 + "\n")

# Mapeo de restaurantes a nuevas categorías
restaurant_categories = {
    "Bigo's": ["snacks", "almuerzos"],
    "Coffee House": ["cafe", "desayunos"],
    "De Lolita": ["almuerzos"],
    "Dogger": ["snacks", "almuerzos"],
    "Dunkin Donuts": ["cafe", "desayunos"],
    "El Tejadito": ["almuerzos"],
    "Frisby": ["snacks", "almuerzos"],
    "Home Food": ["almuerzos"],
    "Juan Valdez Café": ["cafe", "desayunos"],
    "La Cafetería": ["cafe", "desayunos"],
    "Madelo": ["almuerzos"],
    "Mi buñuelo": ["postres", "snacks"],
    "Pimientos": ["almuerzos"],
    "Plural": ["almuerzos"],
    "Subway": ["snacks", "almuerzos"],
    "Taco Factory": ["snacks", "almuerzos"],
    "Aldea Nikkei": ["almuerzos", "snacks"],
}

try:
    # Step 1: Limpiar categorías antiguas
    print("1. Eliminando categorías antiguas...")
    EstablishmentCategory.objects.all().delete()
    print("   ✓ Relaciones eliminadas")
    Category.objects.all().delete()
    print("   ✓ Categorías eliminadas")
    
    # Step 2: Crear nuevas categorías
    print("\n2. Creando nuevas categorías...")
    new_categories = {
        'almuerzos': 'Almuerzos',
        'postres': 'Postres',
        'desayunos': 'Desayunos',
        'snacks': 'Snacks',
        'cafe': 'Café',
    }
    
    categories = {}
    for cat_key, cat_name in new_categories.items():
        cat = Category.objects.create(name=cat_key, description=f'Categoría: {cat_name}')
        categories[cat_key] = cat
        print(f"   ✓ {cat_name} creada")
    
    # Step 3: Reasignar categorías a restaurantes
    print("\n3. Reasignando categorías a restaurantes...")
    for rest_name, cat_keys in restaurant_categories.items():
        try:
            est = Establishment.objects.get(name=rest_name)
            for cat_key in cat_keys:
                if cat_key in categories:
                    EstablishmentCategory.objects.create(
                        establishment=est,
                        category=categories[cat_key]
                    )
            print(f"   ✓ {rest_name} - {', '.join([new_categories[k] for k in cat_keys])}")
        except Establishment.DoesNotExist:
            print(f"   ✗ Restaurante no encontrado: {rest_name}")
        except Exception as e:
            print(f"   ✗ Error con {rest_name}: {e}")
    
    # Verificación
    print("\n" + "="*80)
    print("VERIFICACIÓN")
    print("="*80)
    print(f"\n✓ Total de categorías: {Category.objects.count()}")
    print(f"✓ Total de relaciones: {EstablishmentCategory.objects.count()}")
    
    print("\nCategorías disponibles:")
    for cat in Category.objects.all():
        est_count = cat.establishmentcategory_set.count()
        print(f"  • {cat.get_name_display()} ({est_count} establecimientos)")
    
    print("\n" + "="*80)
    print("✓ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
