from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from ..models import Account


class AccountTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.collection_agency = self.create_collection_agency()
        self.client_model = self.create_client(collection_agency=self.collection_agency)
        self.customer = self.create_customer()

    def test_list_accounts(self):
        account = self.create_account(client=self.client_model, customer=self.customer)
        url = reverse('api:account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_account(self):
        url = reverse('api:account-list')
        data = {
            'client': self.client_model.id,
            'customer': self.customer.ssn,
            'balance': 1000.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.get()
        self.assertEqual(account.balance, 1000.00)

    def test_create_account_400_missing_required_fields(self):
        url = reverse('api:account-list')
        data = {
            'client': self.client_model.id,
            'balance': 1000.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)

    def test_retrieve_account(self):
        account = self.create_account(client=self.client_model, customer=self.customer)
        url = reverse('api:account-detail', args=[account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['balance']), float(account.balance))

    def test_retrieve_account_404(self):
        url = reverse('api:account-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        account = self.create_account(client=self.client_model, customer=self.customer)
        url = reverse('api:account-detail', args=[account.id])
        data = {
            'client': self.client_model.id,
            'customer': self.customer.ssn,
            'balance': 2000.00
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account.refresh_from_db()
        self.assertEqual(account.balance, 2000.00)

    def test_update_account_404(self):
        url = reverse('api:account-detail', args=[999])
        data = {
            'client': self.client_model.id,
            'customer': self.customer.ssn,
            'balance': 2000.00
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        account = self.create_account(client=self.client_model, customer=self.customer)
        url = reverse('api:account-detail', args=[account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

    def test_delete_account_404(self):
        url = reverse('api:account-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_allowed(self):
        account = self.create_account(client=self.client_model, customer=self.customer)
        url = reverse('api:account-detail', args=[account.id])
        response = self.client.patch(url, {'balance': 2000.00})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 