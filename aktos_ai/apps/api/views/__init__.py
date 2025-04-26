from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint showing available endpoints
    """
    return Response({
        'collection_agencies': reverse('api:collection-agency-list', request=request, format=format),
        'clients': reverse('api:client-list', request=request, format=format),
        'customers': reverse('api:customer-list', request=request, format=format),
        'accounts': reverse('api:account-list', request=request, format=format),
        'csv_upload': reverse('api:csv-upload', request=request, format=format),
    }) 