from django.db import models

class Seedbed(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("CLOSED", "Closed"),
    ]

    name = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    tutor = models.CharField(max_length=200, blank=True, default="TBD")
    description = models.TextField(blank=True, default="Description not available yet.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    source_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name