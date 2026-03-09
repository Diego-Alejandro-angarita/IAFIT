import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LlamaIndex.models import Establishment, Category, EstablishmentCategory, Schedule
from datetime import time

print("=" * 80)
print("MIGRANDO DATOS A MODELOS DE DJANGO")
print("=" * 80)

# Datos de restaurantes modificados para el modelo Django
restaurants_data = [
    {
        'name': 'Bigo\'s',
        'description': 'Restaurante y cafetería: menú del día, bowl mexicano, asados y menú de pastas.',
        'establishment_type': 'restaurante',
        'location': 'Cafetería Central, 1er piso.',
        'phone': '+57 310 473 5515',
        'email': 'correobigoseafit@casaalimenticia.com',
        'image_url': '',
        'categories': ['almuerzo'],
        'schedule': {
            1: ('06:00', '20:00'),  # Lun
            2: ('06:00', '20:00'),  # Mar
            3: ('06:00', '20:00'),  # Mié
            4: ('06:00', '20:00'),  # Jue
            5: ('06:00', '20:00'),  # Vie
            6: ('06:00', '14:00'),  # Sáb
            7: None,  # Dom - Cerrado
        }
    },
    {
        'name': 'Coffee House',
        'description': 'Pastelería y café.',
        'establishment_type': 'cafeteria',
        'location': 'Plaza del Centro de Innovación Argos.',
        'phone': '+57 313 661 3630',
        'email': '',
        'image_url': '',
        'categories': ['cafe'],
        'schedule': {
            1: ('05:30', '20:00'),
            2: ('05:30', '20:00'),
            3: ('05:30', '20:00'),
            4: ('05:30', '20:00'),
            5: ('05:30', '20:00'),
            6: ('07:00', '13:00'),
            7: None,
        }
    },
    {
        'name': 'De Lolita',
        'description': 'Café + menú rotativo ("algo nuevo" regularmente).',
        'establishment_type': 'cafeteria',
        'location': 'Bloque 38, frente a las cafeterías Norte.',
        'phone': '+57 318 372 9739',
        'email': 'linagdn@gmail.com',
        'image_url': '',
        'categories': ['cafe'],
        'schedule': {
            1: ('07:00', '20:00'),
            2: ('07:00', '20:00'),
            3: ('07:00', '20:00'),
            4: ('07:00', '20:00'),
            5: ('07:00', '20:00'),
            6: ('07:00', '12:00'),
            7: None,
        }
    },
    {
        'name': 'Dogger',
        'description': 'Perros calientes, hamburguesas, sándwiches, papas fritas, postres y combos estudiantiles.',
        'establishment_type': 'comida_rapida',
        'location': 'Contenedor, Plaza del Estudiante.',
        'phone': '+57 320 671 9937',
        'email': '',
        'image_url': '',
        'categories': ['comida_rapida'],
        'schedule': {
            1: ('10:30', '20:30'),
            2: ('10:30', '20:30'),
            3: ('10:30', '20:30'),
            4: ('10:30', '20:30'),
            5: ('10:30', '20:30'),
            6: ('10:00', '15:00'),
            7: None,
        }
    },
    {
        'name': 'Dunkin Donuts',
        'description': 'Café, sándwiches y donas.',
        'establishment_type': 'cafeteria',
        'location': 'Cafetería Central, zona "burbuja", 2do piso.',
        'phone': '(604) 2626500',
        'email': '',
        'image_url': '',
        'categories': ['cafe'],
        'schedule': {
            1: ('06:00', '20:00'),
            2: ('06:00', '20:00'),
            3: ('06:00', '20:00'),
            4: ('06:00', '20:00'),
            5: ('06:00', '20:00'),
            6: ('07:00', '13:00'),
            7: None,
        }
    },
    {
        'name': 'El Tejadito',
        'description': 'Hojaldres, pandebonos, pasteles salados (queso, carne, pollo, jamón y queso).',
        'establishment_type': 'cafeteria',
        'location': 'Cafetería Norte.',
        'phone': '+57 304 612 4583',
        'email': 'fanery0402@gmail.com',
        'image_url': '',
        'categories': ['postres'],
        'schedule': {
            1: ('06:30', '20:00'),
            2: ('06:30', '20:00'),
            3: ('06:30', '20:00'),
            4: ('06:30', '20:00'),
            5: ('06:30', '20:00'),
            6: ('07:00', '12:30'),
            7: None,
        }
    },
    {
        'name': 'Frisby',
        'description': 'Menú del día, almuerzos, desayunos y postres.',
        'establishment_type': 'restaurante',
        'location': 'Cafetería Central, 1er piso.',
        'phone': '+57 320 670 8240',
        'email': '',
        'image_url': '',
        'categories': ['almuerzo'],
        'schedule': {
            1: ('10:00', '20:30'),
            2: ('10:00', '20:30'),
            3: ('10:00', '20:30'),
            4: ('10:00', '20:30'),
            5: ('10:00', '20:30'),
            6: ('10:00', '15:00'),
            7: None,
        }
    },
    {
        'name': 'Home Food',
        'description': 'Desayunos, menú del día, asados, cazuela de frijoles, pastas y panadería.',
        'establishment_type': 'restaurante',
        'location': 'Cafetería Central, 1er piso.',
        'phone': '+57 304 247 5189',
        'email': '',
        'image_url': '',
        'categories': ['almuerzo'],
        'schedule': {
            1: ('07:00', '20:00'),
            2: ('07:00', '20:00'),
            3: ('07:00', '20:00'),
            4: ('07:00', '20:00'),
            5: ('07:00', '20:00'),
            6: ('07:00', '14:00'),
            7: None,
        }
    },
    {
        'name': 'Juan Valdez Café',
        'description': 'Café colombiano.',
        'establishment_type': 'cafeteria',
        'location': 'Cafetería Norte.',
        'phone': '',
        'email': 'eafit.jv@juanvaldezcafe.com',
        'image_url': '',
        'categories': ['cafe'],
        'schedule': {
            1: ('06:30', '20:30'),
            2: ('06:30', '20:30'),
            3: ('06:30', '20:30'),
            4: ('06:30', '20:30'),
            5: ('06:30', '20:30'),
            6: ('07:00', '14:00'),
            7: None,
        }
    },
    {
        'name': 'La Cafetería',
        'description': 'Desayunos, almuerzos, panadería y pastelería.',
        'establishment_type': 'cafeteria',
        'location': 'Bloque G1 (Idiomas), 5to piso.',
        'phone': '+57 300 333 5768',
        'email': '',
        'image_url': '',
        'categories': ['almuerzo', 'postres'],
        'schedule': {
            1: ('07:00', '19:00'),
            2: ('07:00', '19:00'),
            3: ('07:00', '19:00'),
            4: ('07:00', '19:00'),
            5: ('07:00', '19:00'),
            6: ('07:00', '13:00'),
            7: None,
        }
    },
    {
        'name': 'Madelo',
        'description': 'Helado de yogurt natural.',
        'establishment_type': 'snack',
        'location': 'Contenedor, Parqueadero Sur.',
        'phone': '+57 312 272 3007',
        'email': 'diego@madelo.com.co',
        'image_url': '',
        'categories': ['postres'],
        'schedule': {
            1: ('09:00', '20:00'),
            2: ('09:00', '20:00'),
            3: ('09:00', '20:00'),
            4: ('09:00', '20:00'),
            5: ('09:00', '20:00'),
            6: ('08:00', '16:00'),
            7: None,
        }
    },
    {
        'name': 'Mi buñuelo',
        'description': 'Servicio de cafetería: desayunos variados, jugos naturales y panadería.',
        'establishment_type': 'cafeteria',
        'location': 'Cafetería Central, 2do piso.',
        'phone': '+57 300 659 7469',
        'email': '',
        'image_url': '',
        'categories': ['cafe', 'postres'],
        'schedule': {
            1: ('06:00', '21:00'),
            2: ('06:00', '21:00'),
            3: ('06:00', '21:00'),
            4: ('06:00', '21:00'),
            5: ('06:00', '21:00'),
            6: ('06:00', '15:00'),
            7: None,
        }
    },
    {
        'name': 'Pimientos',
        'description': 'Comida Italiana.',
        'establishment_type': 'restaurante',
        'location': 'Cafetería Norte.',
        'phone': '+57 320 444 2558',
        'email': 'pimientospizza@gmail.com',
        'image_url': '',
        'categories': ['internacional'],
        'schedule': {
            1: ('07:30', '19:45'),
            2: ('07:30', '19:45'),
            3: ('07:30', '19:45'),
            4: ('07:30', '19:45'),
            5: ('07:30', '19:45'),
            6: ('10:00', '15:00'),
            7: None,
        }
    },
    {
        'name': 'Plural',
        'description': 'Comida nutricional "estado de ánimo/saludable", barra para armar al gusto, hamburguesa vegetariana, shawarma.',
        'establishment_type': 'restaurante',
        'location': 'Bloque 38, frente a las cafeterías.',
        'phone': '+57 318 372 9739',
        'email': 'linagdn@gmail.com',
        'image_url': '',
        'categories': ['vegetariano', 'saludable'],
        'schedule': {
            1: ('07:00', '20:00'),
            2: ('07:00', '20:00'),
            3: ('07:00', '20:00'),
            4: ('07:00', '20:00'),
            5: ('07:00', '20:00'),
            6: ('07:00', '12:00'),
            7: None,
        }
    },
    {
        'name': 'Subway',
        'description': 'Sándwiches hechos a la orden con pan fresco, carnes y vegetales.',
        'establishment_type': 'comida_rapida',
        'location': 'Contenedor, Parqueadero Sur.',
        'phone': '+57 316 742 5682',
        'email': 'sub.castro.a@gmail.com',
        'image_url': '',
        'categories': ['comida_rapida'],
        'schedule': {
            1: ('08:00', '20:00'),
            2: ('08:00', '20:00'),
            3: ('08:00', '20:00'),
            4: ('08:00', '20:00'),
            5: ('08:00', '20:00'),
            6: ('08:00', '15:00'),
            7: None,
        }
    },
    {
        'name': 'Taco Factory',
        'description': 'Comida rápida mexicana "gourmet", módulos personalizables y snacks.',
        'establishment_type': 'comida_rapida',
        'location': 'Cafetería Central, 2do piso.',
        'phone': '+57 316 526 9565',
        'email': 'taco-factory@hotmail.com',
        'image_url': '',
        'categories': ['comida_rapida'],
        'schedule': {
            1: ('11:00', '19:00'),
            2: ('11:00', '19:00'),
            3: ('11:00', '19:00'),
            4: ('11:00', '19:00'),
            5: ('11:00', '19:00'),
            6: ('09:30', '14:00'),
            7: None,
        }
    },
    {
        'name': 'Aldea Nikkei',
        'description': 'Comida Peruana y Japonesa: platos a la carta, almuerzos, ensaladas, panadería, café y eventos.',
        'establishment_type': 'restaurante',
        'location': 'Cafetería Central, 1er piso.',
        'phone': '+57 317 365 9038',
        'email': '',
        'image_url': '',
        'categories': ['internacional', 'almuerzo'],
        'schedule': {
            1: ('07:00', '21:00'),
            2: ('07:00', '21:00'),
            3: ('07:00', '21:00'),
            4: ('07:00', '21:00'),
            5: ('07:00', '21:00'),
            6: ('07:00', '14:30'),
            7: None,
        }
    },
]

try:
    # 1. Limpiar datos existentes
    print("\n1. Limpiando datos existentes...")
    Schedule.objects.all().delete()
    EstablishmentCategory.objects.all().delete()
    Establishment.objects.all().delete()
    Category.objects.all().delete()
    print("   ✓ Datos existentes eliminados")
    
    # 2. Crear categorías (si no existen)
    print("\n2. Creando categorías...")
    categories_dict = {}
    category_choices = dict(Category.CATEGORY_CHOICES)
    
    for cat_name, cat_display in category_choices.items():
        cat, created = Category.objects.get_or_create(name=cat_name)
        categories_dict[cat_name] = cat
        status = "✓ Creada" if created else "✓ Existente"
        print(f"   {status}: {cat_display}")
    
    # 3. Crear establecimientos
    print(f"\n3. Creando {len(restaurants_data)} establecimientos...")
    for i, restaurant in enumerate(restaurants_data, 1):
        est = Establishment.objects.create(
            name=restaurant['name'],
            description=restaurant['description'],
            establishment_type=restaurant['establishment_type'],
            location=restaurant['location'],
            phone=restaurant['phone'],
            email=restaurant['email'],
            image_url=restaurant['image_url']
        )
        
        # Asignar categorías
        for cat_name in restaurant['categories']:
            if cat_name in categories_dict:
                EstablishmentCategory.objects.create(
                    establishment=est,
                    category=categories_dict[cat_name]
                )
        
        # Crear horarios
        for day, times in restaurant['schedule'].items():
            if times:  # Si no está cerrado
                opening, closing = times
                opening_time = time(int(opening.split(':')[0]), int(opening.split(':')[1]))
                closing_time = time(int(closing.split(':')[0]), int(closing.split(':')[1]))
                
                Schedule.objects.create(
                    establishment=est,
                    day_of_week=day,
                    opening_time=opening_time,
                    closing_time=closing_time,
                    is_open=True
                )
            else:  # Si está cerrado ese día
                Schedule.objects.create(
                    establishment=est,
                    day_of_week=day,
                    opening_time=time(0, 0),
                    closing_time=time(0, 0),
                    is_open=False
                )
        
        print(f"   ✓ {i}. {restaurant['name']}")
    
    # 4. Verificar
    print("\n4. Verificando datos...")
    est_count = Establishment.objects.count()
    cat_count = Category.objects.count()
    sch_count = Schedule.objects.count()
    
    print(f"   ✓ Establecimientos creados: {est_count}")
    print(f"   ✓ Categorías: {cat_count}")
    print(f"   ✓ Horarios creados: {sch_count}")
    
    print("\n" + "=" * 80)
    print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\n✓ Los datos ahora están disponibles a través de:")
    print("   → http://localhost:8000/api/establishments/")
    print("   → http://localhost:8000/api/categories/")
    print("\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
