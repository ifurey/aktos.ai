import django_filters
from ..models import Account


class AccountFilter(django_filters.FilterSet):
    min_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    customer_id = django_filters.NumberFilter(field_name='customer__id')
    client_id = django_filters.CharFilter(field_name='client__id')
    collection_agency_id = django_filters.NumberFilter(field_name='client__collection_agency__id')

    class Meta:
        model = Account
        fields = ['min_balance', 'max_balance', 'status', 'customer_id', 'client_id', 'collection_agency_id'] 