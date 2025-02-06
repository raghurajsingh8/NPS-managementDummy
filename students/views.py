# students/views.py
from django.shortcuts import render
from .models import Student

def student_list(request):
    # Fetch all student data
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})
