from django.db import models
from user.models import Student
# Create your models here.



class StudentRegister(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    profile_photo = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    date_of_birth=models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    address=models.CharField(max_length=225)


