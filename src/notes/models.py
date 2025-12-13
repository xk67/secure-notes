from django.db import models
from django.conf import settings
import uuid

class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    title = models.CharField(max_length=32)
    content = models.TextField()
    private = models.BooleanField(default=True)
    # How do I handle constraint exceptions caused by duplicate UUID values?
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title