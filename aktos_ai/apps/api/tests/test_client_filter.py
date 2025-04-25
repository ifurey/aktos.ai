from django.test import TestCase
from django_filters import FilterSet
from ..filters.client import ClientFilter
from ..models import Client, CollectionAgency


class ClientFilterTest(TestCase):
    def setUp(self):
        self.agency1 = CollectionAgency.objects.create(name='Agency 1')
        self.agency2 = CollectionAgency.objects.create(name='Agency 2')
        
        self.client1 = Client.objects.create(
            name='Client One',
            collection_agency=self.agency1
        )
        self.client2 = Client.objects.create(
            name='Client Two',
            collection_agency=self.agency2
        )
        self.client3 = Client.objects.create(
            name='Another Client',
            collection_agency=self.agency1
        )

    def test_filter_by_name(self):
        qs = Client.objects.all()
        filtered = ClientFilter({'name': 'Client'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 3)  # All clients have 'Client' in their name
        self.assertIn(self.client1, filtered)
        self.assertIn(self.client2, filtered)
        self.assertIn(self.client3, filtered)

    def test_filter_by_collection_agency_id(self):
        qs = Client.objects.all()
        filtered = ClientFilter({'collection_agency_id': self.agency1.id}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.client1, filtered)
        self.assertIn(self.client3, filtered)
        self.assertNotIn(self.client2, filtered)

    def test_filter_combinations(self):
        qs = Client.objects.all()
        filtered = ClientFilter({
            'name': 'Client',
            'collection_agency_id': self.agency1.id
        }, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)  # Both clients in agency1 have 'Client' in their name
        self.assertIn(self.client1, filtered)
        self.assertIn(self.client3, filtered)
        self.assertNotIn(self.client2, filtered) 