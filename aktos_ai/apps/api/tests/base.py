from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import CollectionAgency, Client, Customer, Account

User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        Account.objects.all().delete()
        Client.objects.all().delete()
        Customer.objects.all().delete()
        CollectionAgency.objects.all().delete()
        super().tearDown()

    def create_collection_agency(self, name='Test Agency'):
        return CollectionAgency.objects.create(name=name)

    def create_client(self, name='Test Client', collection_agency=None):
        if not collection_agency:
            collection_agency = self.create_collection_agency()
        return Client.objects.create(name=name, collection_agency=collection_agency)

    def create_customer(self, ssn='123-45-6789', name='Test Customer', address='123 Test St'):
        return Customer.objects.create(ssn=ssn, name=name, address=address)

    def create_account(self, customer=None, client=None, balance=1000.00, status='active'):
        if not customer:
            customer = self.create_customer()
        if not client:
            client = self.create_client()
        return Account.objects.create(
            customer=customer,
            client=client,
            balance=balance,
            status=status
        ) 