from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    location = models.CharField(max_length=200, verbose_name="Ubicación (Sala/Auditorio)")
    event_date = models.DateField(verbose_name="Fecha del evento")
    event_time = models.TimeField(verbose_name="Hora del evento")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'event_time']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return f"{self.title} - {self.event_date} {self.event_time}"