from django.db import models
from django.conf import settings

class Category(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='time_categories',
    )

    name = models.CharField(max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_name_for_user'),
        ]
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"