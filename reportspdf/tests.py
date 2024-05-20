from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import LabReport
from .forms import LabReportForm
import os

class LabReportTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Define paths for test PDF files
        self.pdf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files', 'fathima.pdf')

    def test_process_lab_report_view_post(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password')

        # Get the initial count of LabReport objects in the database
        initial_count = LabReport.objects.count()

        # Create a test PDF file
        with open(self.pdf_file_path, 'rb') as file:
            pdf_file = SimpleUploadedFile('test_pdf.pdf', file.read(), content_type='application/pdf')

        # Send POST request to the lab report processing view with valid form data
        form_data = {'name': 'Test Report', 'pdf_file': pdf_file}
        response = self.client.post(reverse('process_lab_report'), data=form_data)

        # Check that the lab report was created
        self.assertEqual(LabReport.objects.count(), initial_count + 1)

        # Assert response status code and possibly other aspects of the response
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Clean up test data
        self.user.delete()
