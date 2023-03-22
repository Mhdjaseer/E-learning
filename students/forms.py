from django import forms
from django.forms import ModelForm
from .models import StudentRegister


class studentsRegister(ModelForm):
    class Meta:
        model=StudentRegister
        fields= '__all__'