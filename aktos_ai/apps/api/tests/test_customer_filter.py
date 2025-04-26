from django.test import TestCase
from django_filters import FilterSet
from ..filters.customer import CustomerFilter
from ..models import Customer


class CustomerFilterTest(TestCase):
    def setUp(self):
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
        self.customer3 = Customer.objects.create(
            name='John Smith',
            ssn='111-22-3333',
            address='789 Pine St'
        )

    def test_filter_by_name(self):
        qs = Customer.objects.all()
        filtered = CustomerFilter({'name': 'John'}, queryset=qs).qs
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.customer1, filtered)
        self.assertIn(self.customer3, filtered)
        self.assertNotIn(self.customer2, filtered)
