import uuid
from django.db import models
from .collection_agency import CollectionAgency


class Client(models.Model):
    """Client model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    collection_agency = models.ForeignKey(
        CollectionAgency,
        on_delete=models.CASCADE,
        related_name='clients'
    )

    def __str__(self):
        return self.name or f"Client {self.id}" 