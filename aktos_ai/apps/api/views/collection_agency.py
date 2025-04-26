from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import CollectionAgency
from ..filters import CollectionAgencyFilter
from ..schemas.collection_agency import (
    CollectionAgencySerializer,
    CollectionAgencyCreateSerializer,
    CollectionAgencyUpdateSerializer
)


class CollectionAgencyViewSet(viewsets.ModelViewSet):
    queryset = CollectionAgency.objects.all().order_by('name')
    serializer_class = CollectionAgencySerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    filterset_class = CollectionAgencyFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionAgencyCreateSerializer
        elif self.action == 'update':
            return CollectionAgencyUpdateSerializer
        return CollectionAgencySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT) 