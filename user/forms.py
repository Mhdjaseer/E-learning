from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Teacher, Student,StudentDetials



class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

class TeacherCreateForm(UserCreateForm):
    class Meta:
        model = Teacher
        
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2',]

class StudentCreateForm(UserCreateForm):
    class Meta:
        model = Student
        Student.is_student=True
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', ]

class StudentDetialsForm(forms.ModelForm):
    
    class Meta:
        model = StudentDetials
        exclude = ['user']
        fields = ['address', 'place']
        

    