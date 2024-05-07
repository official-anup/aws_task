from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.create_customer, name='create_customer'),
    path('list-customers/', views.list_customers, name='list_customers'),


]
