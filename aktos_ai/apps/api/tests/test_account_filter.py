from django.test import TestCase
from django_filters import FilterSet
from ..filters.account import AccountFilter
from ..models import Account, Customer, Client, CollectionAgency


class AccountFilterTest(TestCase):
    def setUp(self):
        # Create agencies
        self.agency1 = CollectionAgency.objects.create(name='Agency 1')
        self.agency2 = CollectionAgency.objects.create(name='Agency 2')
        
        # Create clients
        self.client1 = Client.objects.create(
            name='Client One',
            collection_agency=self.agency1
        )
        self.client2 = Client.objects.create(
            name='Client Two',
            collection_agency=self.agency2
        )
        
        # Create customers
        self.customer1 = Customer.objects.create(
            name='John Doe',
            ssn='123-45-6789',
            address='123 Main St'
        )
        self.customer2 = Customer.objects.create(
            name='Jane Smith',
            ssn='987-65-4321',
            address='456 Oak St'
        )
        
        # Create accounts
        self.account1 = Account.objects.create(
            balance=1000.00,
            status=Account.Status.IN_COLLECTION,
            customer=self.customer1,
            client=self.client1
        )
        self.account2 = Account.objects.create(
            balance=2000.00,
            status=Account.Status.INACTIVE,
            customer=self.customer2,
            client=self.client2
        )
        self.account3 = Account.objects.create(
            balance=500.00,
            status=Account.Status.IN_COLLECTION,
            customer=self.customer1,
            client=self.client1
        )

    def test_filter_by_min_balance(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'min_balance': 1000}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account2, filtered)
        self.assertNotIn(self.account3, filtered)

    def test_filter_by_max_balance(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'max_balance': 1000}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_by_status(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'status': Account.Status.IN_COLLECTION}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_by_customer_name(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'customer_name': 'John'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_by_customer_id(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'customer_id': self.customer1.id}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_by_client_id(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'client_id': self.client1.id}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_by_collection_agency_id(self):
        qs = Account.objects.all()
        filtered = AccountFilter({'collection_agency_id': self.agency1.id}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.account1, filtered)
        self.assertIn(self.account3, filtered)
        self.assertNotIn(self.account2, filtered)

    def test_filter_combinations(self):
        qs = Account.objects.all()
        filtered = AccountFilter({
            'min_balance': 1000,
            'status': Account.Status.IN_COLLECTION,
            'client_id': self.client1.id
        }, queryset=qs).qs
        self.assertEqual(filtered.count(), 1)
        self.assertIn(self.account1, filtered)
        self.assertNotIn(self.account2, filtered)
        self.assertNotIn(self.account3, filtered) 