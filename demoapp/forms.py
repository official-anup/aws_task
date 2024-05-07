from django import forms
from .models import CustomerDocumentModel

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = CustomerDocumentModel
        fields = ['attached_file']
