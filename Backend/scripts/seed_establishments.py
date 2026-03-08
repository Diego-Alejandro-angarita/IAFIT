"""
Script para poblar la base de datos con establecimientos gastronómicos de ejemplo
"""
import os
import django
from datetime import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LlamaIndex.models import Establishment, Category, EstablishmentCategory, Schedule, Menu

# Limpiar datos existentes
print("Limpiando datos existentes...")
Establishment.objects.all().delete()
Category.objects.all().delete()

# Crear categorías
print("Creando categorías...")
categories_data = [
    ('almuerzo', 'Almuerzo'),
    ('cafe', 'Café'),
    ('vegetariano', 'Vegetariano'),
    ('postres', 'Postres'),
    ('bebidas', 'Bebidas'),
    ('comida_rapida', 'Comida Rápida'),
    ('internacional', 'Comida Internacional'),
    ('saludable', 'Opción Saludable'),
]

categories = {}
for name, display_name in categories_data:
    cat, created = Category.objects.get_or_create(name=name)
    categories[name] = cat
    print(f"  ✓ {display_name}")

# Crear establecimientos
print("\nCreando establecimientos...")
establishments_data = [
    {
        'name': 'Cafetería Central',
        'type': 'cafeteria',
        'location': 'Edificio A - Piso 1',
        'description': 'Cafetería principal del campus con variedad de bebidas y pan dulce',
        'phone': '(555) 1234567',
        'email': 'cafeteria@eafit.edu.co',
        'image_url': 'https://via.placeholder.com/400x300?text=Cafetería+Central',
        'categories': ['cafe', 'postres', 'bebidas'],
        'schedules': {
            1: ('06:30', '18:00'),  # Lunes
            2: ('06:30', '18:00'),  # Martes
            3: ('06:30', '18:00'),  # Miércoles
            4: ('06:30', '18:00'),  # Jueves
            5: ('06:30', '18:00'),  # Viernes
            6: ('08:00', '14:00'),  # Sábado
            7: None,  # Domingo cerrado
        },
        'menus': [
            {'name': 'Café Americano', 'description': 'Café recién pasado', 'price': '3.50'},
            {'name': 'Capuchino', 'description': 'Café con leche esponjada', 'price': '4.50'},
            {'name': 'Croissant', 'description': 'Croissant de mantequilla', 'price': '2.50'},
        ]
    },
    {
        'name': 'Comedor EAFIT',
        'type': 'restaurante',
        'location': 'Edificio B - Piso 2',
        'description': 'Restaurante principal con menú diario variado',
        'phone': '(555) 2345678',
        'email': 'comedor@eafit.edu.co',
        'image_url': 'https://via.placeholder.com/400x300?text=Comedor+EAFIT',
        'categories': ['almuerzo', 'bebidas', 'saludable'],
        'schedules': {
            1: ('11:00', '14:00'),  # Lunes
            2: ('11:00', '14:00'),  # Martes
            3: ('11:00', '14:00'),  # Miércoles
            4: ('11:00', '14:00'),  # Jueves
            5: ('11:00', '14:00'),  # Viernes
            6: None,  # Sábado cerrado
            7: None,  # Domingo cerrado
        },
        'menus': [
            {'name': 'Almuerzo del Día', 'description': 'Proteína, carbohidrato y ensalada', 'price': '8.50'},
            {'name': 'Almuerzo Vegetariano', 'description': 'Proteína vegetal, carbohidrato y ensalada', 'price': '7.50'},
            {'name': 'Jugo Natural', 'description': 'Jugo fresco del día', 'price': '2.00'},
        ]
    },
    {
        'name': 'Snack Rápido',
        'type': 'snack',
        'location': 'Edificio C - Piso 1',
        'description': 'Snack bar con opciones rápidas y saludables',
        'phone': '(555) 3456789',
        'email': 'snack@eafit.edu.co',
        'image_url': 'https://via.placeholder.com/400x300?text=Snack+Rápido',
        'categories': ['comida_rapida', 'saludable', 'bebidas'],
        'schedules': {
            1: ('07:00', '19:00'),  # Lunes
            2: ('07:00', '19:00'),  # Martes
            3: ('07:00', '19:00'),  # Miércoles
            4: ('07:00', '19:00'),  # Jueves
            5: ('07:00', '19:00'),  # Viernes
            6: ('09:00', '15:00'),  # Sábado
            7: None,  # Domingo cerrado
        },
        'menus': [
            {'name': 'Sándwich de Pollo', 'description': 'Sándwich fresco con pechuga de pollo', 'price': '5.00'},
            {'name': 'Ensalada Caesar', 'description': 'Ensalada con aderezo Caesar', 'price': '6.50'},
            {'name': 'Batido de Frutas', 'description': 'Batido natural de frutas', 'price': '3.50'},
        ]
    },
    {
        'name': 'Pizzería Italiana',
        'type': 'comida_rapida',
        'location': 'Edificio A - Piso 2',
        'description': 'Auténtica pizzería italiana con opciones vegetarianas',
        'phone': '(555) 4567890',
        'email': 'pizza@eafit.edu.co',
        'image_url': 'https://via.placeholder.com/400x300?text=Pizzería+Italiana',
        'categories': ['comida_rapida', 'internacional', 'vegetariano'],
        'schedules': {
            1: ('12:00', '20:00'),  # Lunes
            2: ('12:00', '20:00'),  # Martes
            3: ('12:00', '20:00'),  # Miércoles
            4: ('12:00', '20:00'),  # Jueves
            5: ('12:00', '21:00'),  # Viernes
            6: ('12:00', '21:00'),  # Sábado
            7: ('12:00', '20:00'),  # Domingo
        },
        'menus': [
            {'name': 'Pizza Margherita', 'description': 'Tomate, mozzarella y albahaca', 'price': '9.50'},
            {'name': 'Pizza Vegetariana', 'description': 'Variedad de verduras frescas', 'price': '8.50'},
            {'name': 'Pizza Pepperoni', 'description': 'Con pepperoni gourmet', 'price': '10.00'},
        ]
    },
    {
        'name': 'Juice Bar',
        'type': 'cafeteria',
        'location': 'Edificio D - Piso 1',
        'description': 'Bar de jugos naturales y smoothies saludables',
        'phone': '(555) 5678901',
        'email': 'juice@eafit.edu.co',
        'image_url': 'https://via.placeholder.com/400x300?text=Juice+Bar',
        'categories': ['bebidas', 'saludable', 'vegetariano'],
        'schedules': {
            1: ('07:00', '17:00'),  # Lunes
            2: ('07:00', '17:00'),  # Martes
            3: ('07:00', '17:00'),  # Miércoles
            4: ('07:00', '17:00'),  # Jueves
            5: ('07:00', '18:00'),  # Viernes
            6: ('09:00', '14:00'),  # Sábado
            7: None,  # Domingo cerrado
        },
        'menus': [
            {'name': 'Jugo de Naranja', 'description': 'Jugo natural de naranja fresca', 'price': '2.50'},
            {'name': 'Smoothie Verde', 'description': 'Smoothie con espinaca y manzana', 'price': '4.00'},
            {'name': 'Smoothie de Frutos Rojos', 'description': 'Mix de frutos rojos con yogur', 'price': '4.50'},
        ]
    },
]

for est_data in establishments_data:
    print(f"\n  Creando: {est_data['name']}")
    
    # Crear establecimiento
    establishment = Establishment.objects.create(
        name=est_data['name'],
        establishment_type=est_data['type'],
        location=est_data['location'],
        description=est_data['description'],
        phone=est_data['phone'],
        email=est_data['email'],
        image_url=est_data['image_url'],
    )
    
    # Agregar categorías
    for cat_name in est_data['categories']:
        if cat_name in categories:
            EstablishmentCategory.objects.create(
                establishment=establishment,
                category=categories[cat_name]
            )
    
    # Agregar horarios
    for day, time_range in est_data['schedules'].items():
        if time_range:
            opening_time = time(*map(int, time_range[0].split(':')))
            closing_time = time(*map(int, time_range[1].split(':')))
            Schedule.objects.create(
                establishment=establishment,
                day_of_week=day,
                opening_time=opening_time,
                closing_time=closing_time,
                is_open=True
            )
        else:
            # Crear entrada con is_open=False para días cerrados
            Schedule.objects.create(
                establishment=establishment,
                day_of_week=day,
                opening_time=time(0, 0),
                closing_time=time(0, 0),
                is_open=False
            )
    
    # Agregar menús
    for menu_data in est_data['menus']:
        Menu.objects.create(
            establishment=establishment,
            name=menu_data['name'],
            description=menu_data['description'],
            price=menu_data['price'],
            available=True
        )
    
    print(f"    ✓ Establecimiento creado")
    print(f"    ✓ Horarios añadidos")
    print(f"    ✓ Menús añadidos")

print("\n✅ Base de datos poblada exitosamente!")
