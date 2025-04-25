from rest_framework import serializers
from ..models import CollectionAgency


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    collection_agency_id = serializers.IntegerField()

    def validate_collection_agency_id(self, value):
        try:
            self.context['collection_agency'] = CollectionAgency.objects.get(id=value)
            return value
        except CollectionAgency.DoesNotExist:
            raise serializers.ValidationError("Collection agency not found")