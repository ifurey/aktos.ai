import uuid
from django.db import models
from .customer import Customer
from .client import Client


class Account(models.Model):
    """Account model representing a debt"""
    class Status(models.TextChoices):
        PAID_IN_FULL = 'PAID_IN_FULL', 'Paid in Full'
        IN_COLLECTION = 'IN_COLLECTION', 'In Collection'
        INACTIVE = 'INACTIVE', 'Inactive'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_COLLECTION
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Account {self.id} - {self.customer.name} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['customer']),
            models.Index(fields=['client']),
        ] 