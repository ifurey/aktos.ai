import django_filters
from ..models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    client_id = django_filters.NumberFilter(field_name='client__id')

    class Meta:
        model = Customer
        fields = ['name', 'client_id'] 