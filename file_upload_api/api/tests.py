from django.test import TestCase
from .models import File
from rest_framework.test import APITestCase,APIClient
from file_upload_api.sample_tasks import upload_file
from django.urls import reverse
from datetime import datetime
from rest_framework import status
import time
today = datetime.today
test_today = today().strftime("%Y-%m-%d")


class TestModel(TestCase):

    def test_str(self):
        file = File.objects.create(file='test.txt',
                                   uploaded_at=today(),
                                   processed=False)
        self.assertEqual(test_today, str(file))

    def test_proccesed(self):
        file = File.objects.create(file='test.txt',
                                   uploaded_at=today(),
                                   processed=True)
        self.assertTrue(file.processed)


class TestUrls(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_files(self):
        url = '/api/files'
        response = self.client.get(url,  follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_upload(self):
        url = '/api/upload'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_save_directory(self):
        file= File.objects.create(file='test.txt',
                                   uploaded_at=today(),
                                   processed=False)

        self.assertEqual(file.file.field.upload_to, 'files/')

    def test_file_name(self):
        file = File.objects.create(file='test.txt',
                                   uploaded_at=today(),
                                   processed=False)

        self.assertEqual(file.file, 'test.txt')


class TestFileUpload(TestCase):
    def test_upload_file(self):
        file = File.objects.create(file='files/test.txt',
                                   uploaded_at=today(),
                                   processed=False)
        upload_file(file.id)
        file.refresh_from_db()
        self.assertTrue(file.processed)


class TestFilesView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_files_view(self):
        file1 = File.objects.create(file='files/test.txt',
                                   uploaded_at=today(),
                                   processed=False)
        file2 = File.objects.create(file='files/test1.txt',
                       uploaded_at=today(),
                       processed=False)
        response = self.client.get('/api/files', follow=True)
        self.assertEqual(2, len(response.data))