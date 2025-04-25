from django.test import TestCase
from django_filters import FilterSet
from ..filters.collection_agency import CollectionAgencyFilter
from ..models import CollectionAgency


class CollectionAgencyFilterTest(TestCase):
    def setUp(self):
        self.agency1 = CollectionAgency.objects.create(name='First Collection Agency')
        self.agency2 = CollectionAgency.objects.create(name='Second Collection Agency')
        self.agency3 = CollectionAgency.objects.create(name='Another Agency')

    def test_filter_by_name(self):
        qs = CollectionAgency.objects.all()
        filtered = CollectionAgencyFilter({'name': 'Collection'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.agency1, filtered)
        self.assertIn(self.agency2, filtered)
        self.assertNotIn(self.agency3, filtered)

    def test_filter_by_name_case_insensitive(self):
        qs = CollectionAgency.objects.all()
        filtered = CollectionAgencyFilter({'name': 'collection'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.agency1, filtered)
        self.assertIn(self.agency2, filtered)
        self.assertNotIn(self.agency3, filtered)

    def test_filter_by_partial_name(self):
        qs = CollectionAgency.objects.all()
        filtered = CollectionAgencyFilter({'name': 'First'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 1)
        self.assertIn(self.agency1, filtered)
        self.assertNotIn(self.agency2, filtered)
        self.assertNotIn(self.agency3, filtered) 