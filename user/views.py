from django.shortcuts import render,redirect
from .forms import UserCreateForm, TeacherCreateForm, StudentCreateForm,StudentDetialsForm



from django.contrib.auth import authenticate, login, logout


def index(request):
    return render (request,'index.html',{'user': request.user})

def create_user(request):
    if request.method == 'POST':
        
        form = UserCreateForm(request.POST)
        
        if form.is_valid():
            form.save()
            # do something
            print(" the user creation is success")
    else:
        form = UserCreateForm()
    return render(request, 'create_user.html', {'form': form})

def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # do something
    else:
        form = TeacherCreateForm()
    return render(request, 'create_teacher.html', {'form': form})
# ---------------------------------------------------------
# def success(request):
#     if request.method == 'POST':
#         form = StudentDetialsForm(request.POST)
#         if form.is_valid():
#             student_details = form.save(commit=False)
#             student_details.user = request.user.student
#             student_details.save()
#             return redirect('user:index')
#     else:
#         form = StudentDetialsForm()

#     return render(request,"success.html",{'form':form})

from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import StudentDetials
from .forms import StudentDetialsForm


class success(LoginRequiredMixin, UpdateView):
    model = StudentDetials
    form_class = StudentDetialsForm
    template_name = "success.html"
    success_url = reverse_lazy('user:index')

    def get_object(self, queryset=None):
        # Get the existing StudentDetials instance for the current user
        obj, created = self.model.objects.get_or_create(user=self.request.user.student)
        return obj

    def form_valid(self, form):
        # Set the user field to the Student instance associated with the current user
        form.instance.user = self.request.user.student
        return super().form_valid(form)




def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:success")
    else:
        form = StudentCreateForm()
    return render(request, 'create_student.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('students:index')
            else:
                return redirect('index')
        else:
            return render(request, 'student_login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'student_login.html')

def user_logout(request):
    logout(request)
    return redirect('user:index')