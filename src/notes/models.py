from django.db import models
import uuid

class Note(models.Model):
    #owner = None
    title = models.CharField(max_length=32)
    content = models.TextField()
    private = models.BooleanField(default=True)
    # How do I handle constraint exceptions caused by duplicate UUID values?
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)