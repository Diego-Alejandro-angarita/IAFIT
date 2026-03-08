from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Seedbed

def seedbed_list(request):
    faculty = (request.GET.get("faculty") or "").strip()
    search = (request.GET.get("search") or "").strip()

    seedbeds = Seedbed.objects.filter(status="ACTIVE")

    if faculty:
        seedbeds = seedbeds.filter(faculty=faculty)

    if search:
        seedbeds = seedbeds.filter(name__icontains=search)

    data = list(seedbeds.values(
        "id",
        "name",
        "faculty",
        "tutor",
        "description",
        "status",
        "source_url"
    ))

    return JsonResponse(data, safe=False)


def seedbed_detail(request, seedbed_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, status="ACTIVE")

    data = {
        "id": seedbed.id,
        "name": seedbed.name,
        "faculty": seedbed.faculty,
        "tutor": seedbed.tutor,
        "description": seedbed.description,
        "status": seedbed.status,
        "source_url": seedbed.source_url,
    }

    return JsonResponse(data)