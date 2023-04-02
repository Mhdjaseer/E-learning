from django import forms
from django.contrib.auth.forms import UserChangeForm
from user.models import Student, StudentDetials

class StudentForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ('email', 'first_name', 'last_name')

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetials
        exclude = ['user']
