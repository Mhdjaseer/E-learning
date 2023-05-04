from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator
from twilio.rest import Client
import random
import re
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)



class UserManager(BaseUserManager):
    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing all non-digit characters
        """
        return re.sub(r'\D', '', phone_number)
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    


class Teacher(User):
   def save(self, *args, **kwargs):
        self.is_teacher = True  # Give the teacher  access
        self.is_active=False #giving the active status
        super().save(*args, **kwargs)

class TeacherDetials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/students')
    address=models.CharField(max_length=225)
    place=models.CharField(max_length=50)
    date_of_birth=models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.IntegerField()
  

    def __str__(self):
        return f'{self.user}'
    


class Student(User):
      def save(self, *args, **kwargs):
        self.is_student = True  # Give the student access
        self.is_active=False #giving the active status
        super().save(*args, **kwargs)

class StudentDetials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/students')
    address=models.CharField(max_length=225)
    place=models.CharField(max_length=50)
    date_of_birth=models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.IntegerField()
  

    def __str__(self):
        return f'{self.user}'
    


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=200)
    duration = models.DurationField(default=timedelta(days=365)) # set default to 1 year
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='course_images/')
    category = models.CharField(max_length=200)
    level = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    

class Teacher_Course_Select(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    instructor= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        end_date = self.course.start_date + self.course.duration
        return timezone.now().date() <= end_date
    
    def __str__(self):
        return str(self.instructor)
    
class Purchase(models.Model):
    course = models.ForeignKey(Teacher_Course_Select, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        end_date = self.course.start_date + self.course.duration
        return timezone.now().date() <= end_date
    