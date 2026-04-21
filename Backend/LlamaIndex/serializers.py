from rest_framework import serializers
from .models import Establishment, Category, EstablishmentCategory, Schedule, Menu


class CategorySerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', 'description']
    
    def get_display_name(self, obj):
        return obj.get_name_display()


class ScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = ['id', 'day_of_week', 'day_name', 'opening_time', 'closing_time', 'is_open']
    
    def get_day_name(self, obj):
        return obj.get_day_of_week_display()


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'available']


class EstablishmentSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    schedules = ScheduleSerializer(many=True, read_only=True)
    menus = MenuSerializer(many=True, read_only=True)
    current_status = serializers.SerializerMethodField()
    establishment_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Establishment
        fields = [
            'id',
            'name',
            'description',
            'establishment_type',
            'establishment_type_display',
            'location',
            'phone',
            'email',
            'image_url',
            'categories',
            'schedules',
            'menus',
            'current_status',
            'created_at',
            'updated_at'
        ]
    
    def get_categories(self, obj):
        # Obtener los objetos Category a través de EstablishmentCategory
        from .models import EstablishmentCategory
        establishment_categories = EstablishmentCategory.objects.filter(establishment=obj)
        return [{'id': ec.category.id, 'name': ec.category.name, 'display_name': ec.category.get_name_display()} 
                for ec in establishment_categories]
    
    def get_establishment_type_display(self, obj):
        return obj.get_establishment_type_display()
    
    def get_current_status(self, obj):
        return obj.get_current_status()


class EstablishmentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar establecimientos"""
    categories = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()
    establishment_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Establishment
        fields = [
            'id',
            'name',
            'establishment_type',
            'establishment_type_display',
            'location',
            'image_url',
            'categories',
            'current_status'
        ]
    
    def get_categories(self, obj):
        # Obtener los objetos Category a través de EstablishmentCategory
        from .models import EstablishmentCategory
        establishment_categories = EstablishmentCategory.objects.filter(establishment=obj)
        return [{'id': ec.category.id, 'name': ec.category.name, 'display_name': ec.category.get_name_display()} 
                for ec in establishment_categories]
    
    def get_establishment_type_display(self, obj):
        return obj.get_establishment_type_display()
    
    def get_current_status(self, obj):
        return obj.get_current_status()
