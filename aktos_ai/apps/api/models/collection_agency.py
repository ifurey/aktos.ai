from django.db import models


class CollectionAgency(models.Model):
    """Collection agency model"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Collection Agencies" 