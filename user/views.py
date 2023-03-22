from django.shortcuts import render,redirect
from .forms import UserCreateForm, TeacherCreateForm, StudentCreateForm



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

def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # do something
    else:
        form = StudentCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


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
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')