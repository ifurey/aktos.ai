import io
import csv
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from .base import BaseAPITestCase


class CSVUploadTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.collection_agency = self.create_collection_agency()
        self.url = reverse('api:csv-upload-list')

    def create_test_csv(self, rows):
        csv_file = io.StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=[
            'client reference no',
            'consumer name',
            'consumer address',
            'ssn',
            'balance',
            'status'
        ])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return csv_file.getvalue().encode('utf-8')

    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file"""
        test_data = [{
            'client reference no': '123e4567-e89b-12d3-a456-426614174000',
            'consumer name': 'John Doe',
            'consumer address': '123 Main St',
            'ssn': '123-45-6789',
            'balance': '1000.00',
            'status': 'active'
        }]
        
        csv_content = self.create_test_csv(test_data)
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(
            self.url,
            {
                'file': csv_file,
                'collection_agency_id': self.collection_agency.id
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['results']['created']['clients'], 1)
        self.assertEqual(response.data['results']['created']['customers'], 1)
        self.assertEqual(response.data['results']['created']['accounts'], 1)

    def test_upload_invalid_file_type(self):
        """Test uploading a non-CSV file"""
        txt_file = SimpleUploadedFile("test.txt", b"not a csv file", content_type="text/plain")
        response = self.client.post(
            self.url,
            {
                'file': txt_file,
                'collection_agency_id': self.collection_agency.id
            },
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'File must be CSV')

    def test_upload_without_collection_agency(self):
        """Test uploading without collection agency ID"""
        test_data = [{
            'client reference no': '123e4567-e89b-12d3-a456-426614174000',
            'consumer name': 'John Doe',
            'consumer address': '123 Main St',
            'ssn': '123-45-6789',
            'balance': '1000.00',
            'status': 'active'
        }]
        
        csv_content = self.create_test_csv(test_data)
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_invalid_collection_agency(self):
        """Test uploading with non-existent collection agency ID"""
        test_data = [{
            'client reference no': '123e4567-e89b-12d3-a456-426614174000',
            'consumer name': 'John Doe',
            'consumer address': '123 Main St',
            'ssn': '123-45-6789',
            'balance': '1000.00',
            'status': 'active'
        }]
        
        csv_content = self.create_test_csv(test_data)
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(
            self.url,
            {
                'file': csv_file,
                'collection_agency_id': 99999
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_duplicate_client(self):
        """Test uploading CSV with existing client"""
        test_data = [{
            'client reference no': '123e4567-e89b-12d3-a456-426614174000',
            'consumer name': 'John Doe',
            'consumer address': '123 Main St',
            'ssn': '123-45-6789',
            'balance': '1000.00',
            'status': 'active'
        }]
        
        # Upload first time
        csv_content = self.create_test_csv(test_data)
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        self.client.post(
            self.url,
            {
                'file': csv_file,
                'collection_agency_id': self.collection_agency.id
            },
            format='multipart'
        )

        # Upload same data again
        csv_content = self.create_test_csv(test_data)
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(
            self.url,
            {
                'file': csv_file,
                'collection_agency_id': self.collection_agency.id
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['results']['existing']['clients'], 1)
        self.assertEqual(response.data['results']['existing']['customers'], 1)
        self.assertEqual(response.data['results']['created']['accounts'], 1) 