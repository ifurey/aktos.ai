from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Customer model"""
    ssn = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}-\d{2}-\d{4}$',
                message='SSN must be in format XXX-XX-XXXX'
            )
        ]
    )
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.ssn})"

    class Meta:
        indexes = [
            models.Index(fields=['ssn']),
        ] 