from rest_framework import serializers
from ..models import CollectionAgency


class CollectionAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionAgency
        fields = ['id', 'name']
        read_only_fields = ['id']


class CollectionAgencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionAgency
        fields = ['id', 'name']
        read_only_fields = ['id']


class CollectionAgencyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionAgency
        fields = ['name'] 