from django.shortcuts import render
from django.views.generic import ListView,UpdateView
from .forms import studentsRegister
from user.models import Student
# Create your views here.
# def index(request):
#     context=Student.objects.all()


#     return render(request,"students_detials.html",{'context':context})

class index(ListView):
    model = Student
    form_class=studentsRegister
    template_name = "students_dashbord.html"
    # error