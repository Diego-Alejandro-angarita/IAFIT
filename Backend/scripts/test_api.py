#!/usr/bin/env python
"""
Script para verificar que la API de establecimientos funciona correctamente
"""

import os
import sys
import django
import json

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LlamaIndex.models import Establishment, Category, EstablishmentCategory
from LlamaIndex.serializers import EstablishmentListSerializer

print("\n" + "="*80)
print("VERIFICACIÓN DE API DE ESTABLECIMIENTOS")
print("="*80 + "\n")

try:
    # Verificar establecimientos en BD
    print("1. Establecimientos en base de datos:")
    establishments = Establishment.objects.all()
    print(f"   ✓ Total: {establishments.count()}")
    
    for est in establishments[:3]:
        print(f"   • {est.name}")
    
    # Verificar categorías
    print("\n2. Categorías en base de datos:")
    categories = Category.objects.all()
    print(f"   ✓ Total: {categories.count()}")
    for cat in categories:
        count = cat.establishmentcategory_set.count()
        print(f"   • {cat.get_name_display()} ({count} restaurantes)")
    
    # Verificar relaciones
    print("\n3. Relaciones establecimiento-categoría:")
    for est in establishments[:3]:
        from LlamaIndex.models import EstablishmentCategory
        est_cats = EstablishmentCategory.objects.filter(establishment=est)
        cat_names = ", ".join([ec.category.get_name_display() for ec in est_cats])
        print(f"   • {est.name}: {cat_names}")
    
    # Serializar datos (como lo hace la API)
    print("\n4. Serialización (como retorna la API):")
    serializer = EstablishmentListSerializer(establishments, many=True)
    data = serializer.data
    print(f"   ✓ Total de registros serializados: {len(data)}")
    
    # Mostrar un ejemplo
    if data:
        print("\n   Ejemplo JSON (primer establecimiento):")
        print("   " + json.dumps(data[0], indent=4)[:500])
    
    print("\n" + "="*80)
    print("✓ API debe estar funcionando correctamente")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
