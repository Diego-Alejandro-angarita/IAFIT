import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from research.models import Seedbed
from django.db.models import Count

print(f"Total semilleros en DB: {Seedbed.objects.count()}")
print(f"Activos: {Seedbed.objects.filter(status='ACTIVE').count()}")

print("\nPor facultad:")
faculties = Seedbed.objects.values('faculty').annotate(total=Count('id')).order_by('-total')
for f in faculties:
    print(f"  {f['faculty']}: {f['total']}")

print("\nLista de semilleros:")
for s in Seedbed.objects.all()[:20]:
    print(f"  - {s.name} ({s.faculty})")

if Seedbed.objects.count() > 20:
    print(f"  ... y {Seedbed.objects.count() - 20} más")
