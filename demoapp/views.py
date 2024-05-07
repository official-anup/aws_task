from django.shortcuts import render, redirect
from .models import DocumentSetModel, CustomerModel, CustomerDocumentModel
from .forms import DocumentUploadForm
import boto3
from django.contrib.auth import authenticate, login,logout


def extract_text_from_document(file_path):
    client = boto3.client('textract', region_name='your_region')
    with open(file_path, 'rb') as file:
        response = client.detect_document_text(Document={'Bytes': file.read()})
    extracted_data = {}
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            key = item['Text'].split(':')[0].strip()
            value = item['Text'].split(':')[1].strip()
            extracted_data[key] = value
    return extracted_data

def create_customer(request):
    user_country = request.user.country
    document_sets = DocumentSetModel.objects.filter(countries=user_country)
    form = DocumentUploadForm()

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.customer = request.user
            uploaded_file.save()

            # Call AWS Textract API to extract data from the uploaded file
            extracted_data = extract_text_from_document(uploaded_file.attached_file.path)

            # Create CustomerModel instance based on extracted data
            customer = CustomerModel.objects.create(
                surname=extracted_data.get('Surname', ''),
                firstname=extracted_data.get('Firstname', ''),
                nationality_id=1,  # Replace with actual nationality ID
                gender=extracted_data.get('Gender', ''),
                created_by=request.user
            )

            CustomerDocumentModel.objects.create(
                customer=customer,
                attached_file=uploaded_file,
                extracted_json=extracted_data
            )
            return redirect('list_customers')

    return render(request, 'create_customer.html', {'form': form, 'document_sets': document_sets})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_customer')  # Redirect to create customer page after login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html', {})

def user_logout(request):
    logout(request)
    return redirect('login')



def list_customers(request):
    customers = CustomerModel.objects.filter(created_by=request.user)
    return render(request, 'list_customers.html', {'customers': customers})
