import django_filters
from ..models import CollectionAgency


class CollectionAgencyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = CollectionAgency
        fields = ['name'] 