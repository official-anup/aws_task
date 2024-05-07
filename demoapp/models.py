from django.db import models
from django.contrib.auth.models import User

class CountryModel(models.Model):
    name = models.CharField(max_length=100)

class DocumentSetModel(models.Model):
    name = models.CharField(max_length=100)
    countries = models.ManyToManyField(CountryModel)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.JSONField()

class CustomerModel(models.Model):
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    nationality = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class CustomerDocumentModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to='documents/')
    extracted_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
