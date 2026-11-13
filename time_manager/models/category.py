from django.db import models
from django.conf import settings

class Category(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='time_categories',
        verbose_name='Time record categories',
    )

    name = models.CharField(max_length=150)