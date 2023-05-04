from django import forms
from django.contrib.auth.forms import UserChangeForm
from user.models import Teacher

class StudentForm(UserChangeForm):
    class Meta:
        model =Teacher
        fields = ('phone_number', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Teacher.objects.filter(phone_number=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email



