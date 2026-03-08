from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time

class Establishment(models.Model):
    """Modelo para representar un establecimiento gastronómico"""
    ESTABLISHMENT_TYPES = [
        ('restaurante', 'Restaurante'),
        ('cafeteria', 'Cafetería'),
        ('snack', 'Snack Bar'),
        ('comida_rapida', 'Comida Rápida'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    establishment_type = models.CharField(max_length=50, choices=ESTABLISHMENT_TYPES)
    location = models.CharField(max_length=255)  # e.g., "Edificio A - Piso 2"
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_current_status(self):
        """Obtiene el estado actual (abierto/cerrado) del establecimiento"""
        from django.utils import timezone
        from datetime import datetime, time
        
        now = timezone.now()
        today = now.isoweekday()  # 1=Lunes, 7=Domingo
        
        # Obtener los horarios para hoy
        schedule = self.schedules.filter(day_of_week=today).first()
        
        if not schedule or not schedule.is_open:
            return {
                'status': 'Closed',
                'message': 'Cerrado',
                'current_time': now.strftime('%H:%M'),
            }
        
        current_time = now.time()
        
        if schedule.opening_time <= current_time < schedule.closing_time:
            return {
                'status': 'Open',
                'message': f'Abierto - Cierra a las {schedule.closing_time.strftime("%I:%M %p")}',
                'current_time': now.strftime('%H:%M'),
                'closing_time': schedule.closing_time.strftime('%H:%M'),
            }
        else:
            return {
                'status': 'Closed',
                'message': f'Cerrado - Abre a las {schedule.opening_time.strftime("%I:%M %p")}',
                'current_time': now.strftime('%H:%M'),
                'opening_time': schedule.opening_time.strftime('%H:%M'),
            }


class Category(models.Model):
    """Categorías de establecimientos (e.g., Almuerzo, Café, Vegetariano)"""
    CATEGORY_CHOICES = [
        ('almuerzo', 'Almuerzo'),
        ('cafe', 'Café'),
        ('vegetariano', 'Vegetariano'),
        ('postres', 'Postres'),
        ('bebidas', 'Bebidas'),
        ('comida_rapida', 'Comida Rápida'),
        ('internacional', 'Comida Internacional'),
        ('saludable', 'Opción Saludable'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.get_name_display()


class EstablishmentCategory(models.Model):
    """Relación muchos-a-muchos entre Establishment y Category"""
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('establishment', 'category')
    
    def __str__(self):
        return f"{self.establishment.name} - {self.category.get_name_display()}"


class Schedule(models.Model):
    """Horarios de funcionamiento de un establecimiento"""
    DAYS_OF_WEEK = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField(default=True)  # Falso si el establecimiento está cerrado ese día
    
    class Meta:
        unique_together = ('establishment', 'day_of_week')
    
    def __str__(self):
        return f"{self.establishment.name} - {self.get_day_of_week_display()}: {self.opening_time} - {self.closing_time}"


class Menu(models.Model):
    """Menús ofrecidos por los establecimientos"""
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)  # e.g., "Almuerzo del día", "Desayuno"
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.establishment.name} - {self.name}"
