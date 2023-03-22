from django.shortcuts import render
from django.views.generic import ListView
from .forms import studentsRegister
from user.models import Student
# Create your views here.
# def index(request):
#     context=Student.objects.all()


#     return render(request,"students_detials.html",{'context':context})

class index(ListView):
    model = Student
    template_name = "students_detials.html"