from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from ..models import Customer


class CustomerTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.collection_agency = self.create_collection_agency()
        self.client_model = self.create_client(collection_agency=self.collection_agency)

    def test_list_customers(self):
        customer = self.create_customer()
        url = reverse('api:customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_customer(self):
        url = reverse('api:customer-list')
        data = {
            'ssn': '987-65-4321',
            'name': 'Test Customer',
            'address': '123 Test St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.get()
        self.assertEqual(customer.name, 'Test Customer')
        self.assertEqual(customer.ssn, '987-65-4321')

    def test_create_customer_400_missing_required_fields(self):
        url = reverse('api:customer-list')
        data = {
            'name': 'Test Customer',
            'address': '123 Test St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ssn', response.data)

    def test_create_customer_400_duplicate_ssn(self):
        self.create_customer(ssn='987-65-4321')
        url = reverse('api:customer-list')
        data = {
            'ssn': '987-65-4321',
            'name': 'Test Customer',
            'address': '123 Test St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ssn', response.data)

    def test_retrieve_customer(self):
        customer = self.create_customer()
        url = reverse('api:customer-detail', args=[customer.ssn])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], customer.name)
        self.assertEqual(response.data['ssn'], customer.ssn)

    def test_retrieve_customer_404(self):
        url = reverse('api:customer-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer(self):
        customer = self.create_customer()
        url = reverse('api:customer-detail', args=[customer.ssn])
        data = {
            'name': 'Updated Customer',
            'address': '456 Test St'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, 'Updated Customer')
        self.assertEqual(customer.address, '456 Test St')

    def test_update_customer_404(self):
        url = reverse('api:customer-detail', args=[999])
        data = {
            'name': 'Updated Customer',
            'address': '456 Test St'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_customer(self):
        customer = self.create_customer()
        url = reverse('api:customer-detail', args=[customer.ssn])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_customer_404(self):
        url = reverse('api:customer-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_allowed(self):
        customer = self.create_customer()
        url = reverse('api:customer-detail', args=[customer.ssn])
        response = self.client.patch(url, {'name': 'Updated Customer'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 