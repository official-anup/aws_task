from django.contrib import admin
from .models import CountryModel, DocumentSetModel, CustomerModel, CustomerDocumentModel

admin.site.register(CountryModel)
admin.site.register(DocumentSetModel)
admin.site.register(CustomerModel)
admin.site.register(CustomerDocumentModel)
