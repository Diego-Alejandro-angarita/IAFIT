import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # Probar conexión básica
        cursor.execute('SELECT current_database(), current_user, version();')
        result = cursor.fetchone()
        
        print("=" * 60)
        print("✓ CONEXIÓN A SUPABASE EXITOSA")
        print("=" * 60)
        print(f"✓ Base de datos: {result[0]}")
        print(f"✓ Usuario: {result[1]}")
        print(f"✓ PostgreSQL: {result[2].split(',')[0]}")
        
        # Contar tablas
        cursor.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"✓ Tablas públicas: {table_count}")
        
        # Listar tablas de la app
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'LlamaIndex_%'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n✓ Tablas de la aplicación ({len(tables)}):")
            for table in tables:
                cursor.execute(f"SELECT count(*) FROM {table[0]};")
                count = cursor.fetchone()[0]
                print(f"  - {table[0]}: {count} registros")
        else:
            print("\n⚠ No se encontraron tablas de LlamaIndex (puede que necesites ejecutar migraciones)")
        
        print("\n" + "=" * 60)
        
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {e}")
