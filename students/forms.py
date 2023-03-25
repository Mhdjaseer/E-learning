from django import forms
from django.urls import reverse_lazy
from user.models import User,StudentDetials


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class studentdetials(forms.ModelForm):
    class Meta:
        model=StudentDetials
        fields='__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['profile_id'].widget = forms.HiddenInput()
    
    # def save(self, commit=True):
    #     student_detials = super().save(commit=False)
    #     abc=User.email
    #     if not student_detials.profile_id:
    #         student_detials.profile_id = self.initial['profile_id']
    #     if commit:
    #         student_detials.save()
    #     return student_detials

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetials
        exclude = ['profile_id']