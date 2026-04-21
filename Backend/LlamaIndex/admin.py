from django.contrib import admin
from .models import Event, Establishment, Category, EstablishmentCategory, Schedule, Menu

admin.site.register(Event)

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'establishment_type', 'location', 'phone')
    list_filter = ('establishment_type', 'created_at')
    search_fields = ('name', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('get_name_display', 'description')
    search_fields = ('name',)

@admin.register(EstablishmentCategory)
class EstablishmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('establishment', 'category')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('establishment', 'get_day_of_week_display', 'opening_time', 'closing_time', 'is_open')
    list_filter = ('day_of_week', 'is_open')
    search_fields = ('establishment__name',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'establishment', 'price', 'available')
    list_filter = ('establishment', 'available', 'created_at')
    search_fields = ('name', 'description', 'establishment__name')
    readonly_fields = ('created_at', 'updated_at')
