from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.db.models import Q


class TimeEntry(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='time_entries',
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='time_entries',
    )

    description = models.TextField(blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(ended_at__isnull=True),
                name='one_running_entry_per_user',
            )
        ]

    def clean(self):
        if self.started_at and self.ended_at:
            if self.started_at > self.ended_at:
                raise ValidationError("Ended time must be after started time")
        if self.category_id:
            if self.user_id != self.category.user_id:
                raise ValidationError("User must be the category owner")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)