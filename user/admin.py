from django.contrib import admin
from .models import User,Teacher,Student,StudentDetials,Course,Purchase
# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(StudentDetials)
admin.site.register(Course)
admin.site.register(Purchase)