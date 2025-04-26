from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Account
from ..filters import AccountFilter
from ..schemas.account import (
    AccountSerializer,
    AccountCreateSerializer,
    AccountUpdateSerializer
)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('created_at')
    http_method_names = ['get', 'post', 'put', 'delete']
    filterset_class = AccountFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['customer__name', 'status']
    ordering_fields = ['created_at', 'balance', 'status']
    ordering = ['-created_at']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'min_balance',
                openapi.IN_QUERY,
                description="Minimum balance value",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_balance',
                openapi.IN_QUERY,
                description="Maximum balance value",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Account status (PAID_IN_FULL, IN_COLLECTION, INACTIVE)",
                type=openapi.TYPE_STRING,
                enum=['PAID_IN_FULL', 'IN_COLLECTION', 'INACTIVE']
            ),
            openapi.Parameter(
                'customer_name',
                openapi.IN_QUERY,
                description="Filter by customer name (contains)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'customer_id',
                openapi.IN_QUERY,
                description="Filter by customer ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description="Filter by client ID",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            ),
            openapi.Parameter(
                'collection_agency_id',
                openapi.IN_QUERY,
                description="Filter by collection agency ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by field (prefix with '-' for descending)",
                type=openapi.TYPE_STRING,
                enum=['created_at', '-created_at', 'balance', '-balance', 'status', '-status']
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in customer name and status",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AccountUpdateSerializer
        return AccountSerializer

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