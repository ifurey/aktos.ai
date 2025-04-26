import django_filters
from ..models import Client


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    collection_agency_id = django_filters.NumberFilter(field_name='collection_agency__id')

    class Meta:
        model = Client
        fields = ['name', 'collection_agency_id'] 