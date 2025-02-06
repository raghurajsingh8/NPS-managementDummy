# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Define the URL for the student list page
    path('', views.student_list, name='student_list'),
]
