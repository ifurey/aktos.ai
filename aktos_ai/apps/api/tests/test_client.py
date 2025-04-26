from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from ..models import Client
import uuid


class ClientTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.collection_agency = self.create_collection_agency()

    def test_list_clients(self):
        client = self.create_client(collection_agency=self.collection_agency)
        url = reverse('api:client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_client(self):
        url = reverse('api:client-list')
        data = {
            'name': 'Test Client',
            'collection_agency': self.collection_agency.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        client = Client.objects.get()
        self.assertEqual(client.name, 'Test Client')
        self.assertEqual(response.data['id'], str(client.id))

    def test_create_client_with_custom_id(self):
        custom_id = uuid.uuid4()
        data = {
            'id': str(custom_id),
            'name': 'Test Client',
            'collection_agency': self.collection_agency.id
        }
        url = reverse('api:client-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], str(custom_id))
        self.assertEqual(response.data['name'], 'Test Client')

    def test_create_client_400_missing_required_fields(self):
        url = reverse('api:client-list')
        data = {
            'name': 'Test Client'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('collection_agency', response.data)

    def test_retrieve_client(self):
        client = self.create_client(collection_agency=self.collection_agency)
        url = reverse('api:client-detail', args=[client.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], client.name)
        self.assertEqual(response.data['id'], str(client.id))

    def test_retrieve_client_404(self):
        url = reverse('api:client-detail', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_client(self):
        client = self.create_client(collection_agency=self.collection_agency)
        url = reverse('api:client-detail', args=[client.id])
        data = {
            'name': 'Updated Client',
            'collection_agency': self.collection_agency.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.name, 'Updated Client')

    def test_update_client_404(self):
        url = reverse('api:client-detail', args=[uuid.uuid4()])
        data = {
            'name': 'Updated Client',
            'collection_agency': self.collection_agency.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_client(self):
        client = self.create_client(collection_agency=self.collection_agency)
        url = reverse('api:client-detail', args=[client.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)

    def test_delete_client_404(self):
        url = reverse('api:client-detail', args=[uuid.uuid4()])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_allowed(self):
        client = self.create_client(collection_agency=self.collection_agency)
        url = reverse('api:client-detail', args=[client.id])
        response = self.client.patch(url, {'name': 'Updated Client'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 