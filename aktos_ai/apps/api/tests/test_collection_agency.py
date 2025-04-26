from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from ..models import CollectionAgency


class CollectionAgencyTests(BaseAPITestCase):
    def test_list_collection_agencies(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_collection_agency(self):
        url = reverse('api:collectionagency-list')
        data = {
            'name': 'Test Agency'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CollectionAgency.objects.count(), 1)
        agency = CollectionAgency.objects.get()
        self.assertEqual(agency.name, 'Test Agency')
        self.assertIn('id', response.data)

    def test_create_collection_agency_400_missing_name(self):
        url = reverse('api:collectionagency-list')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_retrieve_collection_agency(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-detail', args=[agency.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], agency.name)
        self.assertEqual(response.data['id'], agency.id)

    def test_retrieve_collection_agency_404(self):
        url = reverse('api:collectionagency-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_collection_agency(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-detail', args=[agency.id])
        data = {
            'name': 'Updated Agency'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agency.refresh_from_db()
        self.assertEqual(agency.name, 'Updated Agency')

    def test_update_collection_agency_400_missing_name(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-detail', args=[agency.id])
        data = {}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_update_collection_agency_404(self):
        url = reverse('api:collectionagency-detail', args=[999])
        data = {'name': 'Updated Agency'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_collection_agency(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-detail', args=[agency.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CollectionAgency.objects.count(), 0)

    def test_delete_collection_agency_404(self):
        url = reverse('api:collectionagency-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_allowed(self):
        agency = self.create_collection_agency()
        url = reverse('api:collectionagency-detail', args=[agency.id])
        response = self.client.patch(url, {'name': 'Updated Agency'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 