from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Teacher, Student,StudentDetials,Course



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


class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetials
        fields = ('image', 'address', 'place', 'date_of_birth', 'gender', 'phone_number')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def save(self, commit=True, user=None):
        if user and not user.is_superuser:
            raise ValueError('Only superusers can create courses')
        return super().save(commit)