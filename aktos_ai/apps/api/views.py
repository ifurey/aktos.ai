from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint, showing available endpoints
    """
    return Response({
        'status': 'ok',
        'message': 'Welcome to the Aktos.ai API',
        'version': '1.0.0',
    })
