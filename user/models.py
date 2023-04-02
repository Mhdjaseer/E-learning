from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

class Teacher(User):
   def save(self, *args, **kwargs):
        self.is_teacher = True  # Give the teacher  access
        super().save(*args, **kwargs)

class Student(User):
      def save(self, *args, **kwargs):
        self.is_student = True  # Give the student access
        self.is_active=True #giving the active status
        super().save(*args, **kwargs)

class StudentDetials(models.Model):
    user=models.ForeignKey(Student, verbose_name=("student_detials"), on_delete=models.CASCADE)
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
    phone_number = models.CharField(max_length=20)
    address=models.CharField(max_length=225)

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
    
class Purchase(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        end_date = self.course.start_date + self.course.duration
        return timezone.now().date() <= end_date