import csv
import io
import uuid

from django.db import transaction
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Client, Customer, Account
from ..schemas.csv_upload import CSVUploadSerializer


class CSVUploadViewSet(viewsets.GenericViewSet):
    serializer_class = CSVUploadSerializer

    # TODO: CSV Upload need file sanitization and validation to avoid malicious files that could exploit CSV Injection,
    #  Memory Exhaustion and  Type Spoofing attacks.
    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        collection_agency = serializer.context['collection_agency']

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File must be CSV'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            results = {
                'created': {'clients': 0, 'customers': 0, 'accounts': 0},
                'existing': {'clients': 0, 'customers': 0},
                'errors': []
            }

            for row in csv_data:
                try:
                    with transaction.atomic():
                        # Process Client
                        client_id = uuid.UUID(row['client reference no'])
                        client, client_created = Client.objects.get_or_create(
                            id=client_id,
                            collection_agency=collection_agency,
                            defaults={'name': None}
                        )
                        if client_created:
                            results['created']['clients'] += 1
                        else:
                            results['existing']['clients'] += 1

                        # Process Customer
                        customer, customer_created = Customer.objects.get_or_create(
                            ssn=row['ssn'],
                            defaults={
                                'name': row['consumer name'],
                                'address': row['consumer address']
                            }
                        )
                        if customer_created:
                            results['created']['customers'] += 1
                        else:
                            results['existing']['customers'] += 1

                        # Create Account
                        Account.objects.create(
                            id=uuid.uuid4(),
                            customer=customer,
                            client=client,
                            balance=row['balance'],
                            status=row['status']
                        )
                        results['created']['accounts'] += 1

                except Exception as e:
                    results['errors'].append({
                        'row': row['client reference no'],
                        'error': str(e)
                    })
                    continue

            return Response({
                'message': 'File processed successfully',
                'results': results
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': f'Error processing file: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)