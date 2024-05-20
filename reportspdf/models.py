from django.db import models

class LabReport(models.Model):
    name = models.CharField(max_length=100, default='Default Name',null=True)

    pdf_file = models.FileField(upload_to='lab_reports/')
