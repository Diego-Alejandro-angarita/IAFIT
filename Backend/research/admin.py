from django.contrib import admin
from .models import Seedbed

@admin.register(Seedbed)
class SeedbedAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty", "tutor", "status")
    list_filter = ("status", "faculty")
    search_fields = ("name", "faculty", "tutor")