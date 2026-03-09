import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Datos de los 17 restaurantes
restaurants_data = [
    {
        'name': 'Bigo\'s',
        'description': 'Restaurante y cafetería: menú del día, bowl mexicano, asados y menú de pastas.',
        'location': 'Cafetería Central, 1er piso.',
        'schedule': 'Lun-Vie 6:00 am - 8:00 pm; Sáb 6:00 am - 2:00 pm',
        'contact_info': 'Alba Lucia Urrego, +57 310 473 5515, correobigoseafit@casaalimenticia.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/wgvjgvjbwf/biggos-menu',
        'content_to_embed': 'Restaurante Bigo\'s en Cafetería Central, 1er piso. Ofrece bowl mexicano, asados y pastas. Horario: Lun-Vie 6am-8pm, Sáb 6am-2pm. Contacto: Alba Lucia Urrego. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Coffee House',
        'description': 'Pastelería y café.',
        'location': 'Plaza del Centro de Innovación Argos.',
        'schedule': 'Lun-Vie 5:30 am - 8:00 pm; Sáb 7:00 am - 1:00 pm',
        'contact_info': '+57 313 661 3630, (604) 261 9698.',
        'menu_link': 'https://universidadeafit.widen.net/s/jpdf5w52r8/coffee-house-menu',
        'content_to_embed': 'Coffee House en Plaza del Centro de Innovación Argos. Ofrece pastelería y café. Horario: Lun-Vie 5:30am-8pm, Sáb 7am-1pm.'
    },
    {
        'name': 'De Lolita',
        'description': 'Café + menú rotativo ("algo nuevo" regularmente).',
        'location': 'Bloque 38, frente a las cafeterías Norte.',
        'schedule': 'Lun-Vie 7:00 am - 8:00 pm; Sáb 7:00 am - 12:00 pm',
        'contact_info': 'Lina Maria Rios, +57 318 372 9739, linagdn@gmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/ffw5mlhtfj/menu-de-lolita',
        'content_to_embed': 'De Lolita en Bloque 38, frente a cafeterías Norte. Ofrece café y menú rotativo. Horario: Lun-Vie 7am-8pm, Sáb 7am-12pm. Contacto: Lina Maria Rios.'
    },
    {
        'name': 'Dogger',
        'description': 'Perros calientes, hamburguesas, sándwiches, papas fritas, postres y combos estudiantiles.',
        'location': 'Contenedor, Plaza del Estudiante.',
        'schedule': 'Lun-Vie 10:30 am - 8:30 pm; Sáb 10:00 am - 3:00 pm',
        'contact_info': 'Alejandro Restrepo (+57 320 671 9937) / Lorraine Marin (+57 301 413 4237).',
        'menu_link': 'https://universidadeafit.widen.net/s/nrh9zs2xrt/menu-dogger',
        'content_to_embed': 'Dogger en Contenedor, Plaza del Estudiante. Ofrece comida rápida: perros, hamburguesas, combos. Horario: Lun-Vie 10:30am-8:30pm, Sáb 10am-3pm.'
    },
    {
        'name': 'Dunkin Donuts',
        'description': 'Café, sándwiches y donas.',
        'location': 'Cafetería Central, zona "burbuja", 2do piso.',
        'schedule': 'Lun-Vie 6:00 am - 8:00 pm; Sáb 7:00 am - 1:00 pm',
        'contact_info': 'Astrid Uribe, (604) 2626500 ext. 101.',
        'menu_link': 'https://universidadeafit.widen.net/s/kp21f2s2bh/menu-dunkin-donuts',
        'content_to_embed': 'Dunkin Donuts en Cafetería Central, burbuja 2do piso. Ofrece café, sándwiches y donas. Horario: Lun-Vie 6am-8pm, Sáb 7am-1pm. Contacto: Astrid Uribe.'
    },
    {
        'name': 'El Tejadito',
        'description': 'Hojaldres, pandebonos, pasteles salados (queso, carne, pollo, jamón y queso).',
        'location': 'Cafetería Norte.',
        'schedule': 'Lun-Vie 6:30 am - 8:00 pm; Sáb 7:00 am - 12:30 pm',
        'contact_info': 'Fanery Alvarez, +57 304 612 4583, fanery0402@gmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/bzrrdfpn8t/tejadito-menu',
        'content_to_embed': 'El Tejadito en Cafetería Norte. Ofrece hojaldres, pandebonos y pasteles salados. Horario: Lun-Vie 6:30am-8pm, Sáb 7am-12:30pm. Contacto: Fanery Alvarez.'
    },
    {
        'name': 'Frisby',
        'description': 'Menú del día, almuerzos, desayunos y postres.',
        'location': 'Cafetería Central, 1er piso.',
        'schedule': 'Lun-Vie 10:00 am - 8:30 pm; Sáb 10:00 am - 3:00 pm',
        'contact_info': '+57 320 670 8240.',
        'menu_link': 'https://universidadeafit.widen.net/s/lwvrg5lwkx/menu-frisby',
        'content_to_embed': 'Restaurante Frisby en Cafetería Central, 1er piso. Ofrece almuerzos y pollo. Horario: Lun-Vie 10am-8:30pm, Sáb 10am-3pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Home Food',
        'description': 'Desayunos, menú del día, asados, cazuela de frijoles, pastas y panadería.',
        'location': 'Cafetería Central, 1er piso.',
        'schedule': 'Lun-Vie 7:00 am - 8:00 pm; Sáb 7:00 am - 2:00 pm',
        'contact_info': 'Admin: +57 304 247 5189; Eventos: +57 304 353 4704; IG: Hood.catering.',
        'menu_link': 'https://universidadeafit.widen.net/s/kbgmlx5mc5/menu-home-food',
        'content_to_embed': 'Home Food en Cafetería Central, 1er piso. Ofrece asados, cazuela de frijoles, pastas. Horario: Lun-Vie 7am-8pm, Sáb 7am-2pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Juan Valdez Café',
        'description': 'Café colombiano.',
        'location': 'Cafetería Norte.',
        'schedule': 'Lun-Vie 6:30 am - 8:30 pm; Sáb 7:00 am - 2:00 pm',
        'contact_info': 'eafit.jv@juanvaldezcafe.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/gpctxtgphv/juan-valdez-menu',
        'content_to_embed': 'Juan Valdez Café en Cafetería Norte. Ofrece café colombiano. Horario: Lun-Vie 6:30am-8:30pm, Sáb 7am-2pm.'
    },
    {
        'name': 'La Cafetería',
        'description': 'Desayunos, almuerzos, panadería y pastelería.',
        'location': 'Bloque G1 (Idiomas), 5to piso.',
        'schedule': 'Lun-Vie 7:00 am - 7:00 pm; Sáb 7:00 am - 1:00 pm',
        'contact_info': 'Cristina Bedoya, +57 300 333 5768 / Nancy Ruiz, +57 314 647 6453.',
        'menu_link': 'https://universidadeafit.widen.net/s/whd9mtdcsh/menu-la-cafeteria',
        'content_to_embed': 'La Cafetería en Bloque G1 (Idiomas), 5to piso. Ofrece desayunos y almuerzos. Horario: Lun-Vie 7am-7pm, Sáb 7am-1pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Madelo',
        'description': 'Helado de yogurt natural.',
        'location': 'Contenedor, Parqueadero Sur.',
        'schedule': 'Lun-Vie 9:00 am - 8:00 pm; Sáb 8:00 am - 4:00 pm',
        'contact_info': 'Diego Alejandro Valencia, +57 312 272 3007, diego@madelo.com.co.',
        'menu_link': 'https://universidadeafit.widen.net/s/hgmsqvxdcv/menu-madelo',
        'content_to_embed': 'Madelo en Contenedor, Parqueadero Sur. Ofrece helado de yogurt natural. Horario: Lun-Vie 9am-8pm, Sáb 8am-4pm. Contacto: Diego Alejandro Valencia.'
    },
    {
        'name': 'Mi buñuelo',
        'description': 'Servicio de cafetería: desayunos variados, jugos naturales y panadería.',
        'location': 'Cafetería Central, 2do piso.',
        'schedule': 'Lun-Vie 6:00 am - 9:00 pm; Sáb 6:00 am - 3:00 pm',
        'contact_info': 'Doira Gomez, +57 300 659 7469 / Sergio Lebrum, +57 311 617 9326.',
        'menu_link': 'https://universidadeafit.widen.net/s/nr8dmdmvbg/menu-mi-bunuelo',
        'content_to_embed': 'Mi buñuelo en Cafetería Central, 2do piso. Ofrece desayunos y jugos naturales. Horario: Lun-Vie 6am-9pm, Sáb 6am-3pm.'
    },
    {
        'name': 'Pimientos',
        'description': 'Comida Italiana.',
        'location': 'Cafetería Norte.',
        'schedule': 'Lun-Vie 7:30 am - 7:45 pm; Sáb 10:00 am - 3:00 pm',
        'contact_info': 'Andres Felipe Pimiento, +57 320 444 2558, pimientospizza@gmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/b6ffzgpz6q/menu-pimientos',
        'content_to_embed': 'Restaurante Pimientos en Cafetería Norte. Ofrece comida italiana. Horario: Lun-Vie 7:30am-7:45pm, Sáb 10am-3pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Plural',
        'description': 'Comida nutricional "estado de ánimo/saludable", barra para armar al gusto, hamburguesa vegetariana, shawarma.',
        'location': 'Bloque 38, frente a las cafeterías.',
        'schedule': 'Lun-Vie 7:00 am - 8:00 pm; Sáb 7:00 am - 12:00 pm',
        'contact_info': 'Lina Maria Rios, +57 318 372 9739, linagdn@gmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/9tcpwcjjpn/menu-plural',
        'content_to_embed': 'Plural en Bloque 38, frente a cafeterías. Ofrece comida saludable y nutritiva, opciones vegetarianas. Horario: Lun-Vie 7am-8pm, Sáb 7am-12pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Subway',
        'description': 'Sándwiches hechos a la orden con pan fresco, carnes y vegetales.',
        'location': 'Contenedor, Parqueadero Sur.',
        'schedule': 'Lun-Vie 8:00 am - 8:00 pm; Sáb 8:00 am - 3:00 pm',
        'contact_info': 'Andrea Castro, +57 316 742 5682, sub.castro.a@gmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/dqjm2vf9zh/menu-subway',
        'content_to_embed': 'Subway en Contenedor, Parqueadero Sur. Ofrece sándwiches a la orden. Horario: Lun-Vie 8am-8pm, Sáb 8am-3pm. Contacto: Andrea Castro.'
    },
    {
        'name': 'Taco Factory',
        'description': 'Comida rápida mexicana "gourmet", módulos personalizables y snacks.',
        'location': 'Cafetería Central, 2do piso.',
        'schedule': 'Lun-Vie 11:00 am - 7:00 pm; Sáb 9:30 am - 2:00 pm',
        'contact_info': 'Luz Maria Roldán, WP: +57 316 526 9565, taco-factory@hotmail.com.',
        'menu_link': 'https://universidadeafit.widen.net/s/dk8cpphrzr/menu-taco-factory',
        'content_to_embed': 'Taco Factory en Cafetería Central, 2do piso. Ofrece comida rápida mexicana gourmet. Horario: Lun-Vie 11am-7pm, Sáb 9:30am-2pm. Menú del día a 20.000 COP de 12pm a 2pm.'
    },
    {
        'name': 'Aldea Nikkei',
        'description': 'Comida Peruana y Japonesa: platos a la carta, almuerzos, ensaladas, panadería, café y eventos.',
        'location': 'Cafetería Central, 1er piso.',
        'schedule': 'Lun-Vie 7:00 am - 9:00 pm; Sáb 7:00 am - 2:30 pm',
        'contact_info': 'Sandra López Arias, +57 317 365 9038.',
        'menu_link': 'https://universidadeafit.widen.net/s/fv5hl2brpk/aldea-nikei-menu',
        'content_to_embed': 'Restaurante Aldea Nikkei ubicado en Cafetería Central, 1er piso. Ofrece comida peruana y japonesa. Horario: Lun-Vie 7am-9pm, Sáb 7am-2:30pm. Contacto: Sandra López Arias. Menú del día a 20.000 COP de 12pm a 2pm.'
    }
]

def main():
    print("=" * 60)
    print("POBLANDO BASE DE DATOS DE RESTAURANTES")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # 1. Habilitar extensión pgvector
        print("\n1. Habilitando extensión pgvector...")
        try:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            print("   ✓ Extensión pgvector habilitada")
        except Exception as e:
            print(f"   ⚠ Advertencia al habilitar pgvector: {e}")
        
        # 2. Verificar si la tabla existe
        print("\n2. Verificando tabla 'restaurants'...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'restaurants'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("   ✓ Tabla 'restaurants' ya existe")
            # Limpiar datos existentes
            print("   → Limpiando datos existentes...")
            cursor.execute("DELETE FROM restaurants;")
            print("   ✓ Datos existentes eliminados")
        else:
            # 3. Crear la tabla
            print("   → Creando tabla 'restaurants'...")
            cursor.execute("""
                CREATE TABLE restaurants (
                    id SERIAL PRIMARY KEY,
                    restaurant_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    location TEXT NOT NULL,
                    schedule TEXT NOT NULL,
                    contact_info TEXT,
                    menu_link TEXT,
                    content_to_embed TEXT NOT NULL,
                    embedding vector(384)
                );
            """)
            print("   ✓ Tabla 'restaurants' creada")
        
        # 4. Insertar los 17 restaurantes
        print(f"\n3. Insertando {len(restaurants_data)} restaurantes...")
        for i, restaurant in enumerate(restaurants_data, 1):
            cursor.execute("""
                INSERT INTO restaurants (
                    restaurant_name, description, location, schedule, 
                    contact_info, menu_link, content_to_embed
                ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                restaurant['name'],
                restaurant['description'],
                restaurant['location'],
                restaurant['schedule'],
                restaurant['contact_info'],
                restaurant['menu_link'],
                restaurant['content_to_embed']
            ))
            print(f"   ✓ {i}. {restaurant['name']}")
        
        # 5. Verificar datos insertados
        print("\n4. Verificando datos insertados...")
        cursor.execute("SELECT COUNT(*) FROM restaurants;")
        count = cursor.fetchone()[0]
        print(f"   ✓ Total de restaurantes en la base de datos: {count}")
        
        # Mostrar algunos registros
        cursor.execute("""
            SELECT restaurant_name, location 
            FROM restaurants 
            ORDER BY restaurant_name 
            LIMIT 5;
        """)
        sample_records = cursor.fetchall()
        print("\n   Muestra de registros:")
        for record in sample_records:
            print(f"     • {record[0]} - {record[1]}")
        
    print("\n" + "=" * 60)
    print("✓ BASE DE DATOS POBLADA EXITOSAMENTE")
    print("=" * 60)

if __name__ == '__main__':
    main()
