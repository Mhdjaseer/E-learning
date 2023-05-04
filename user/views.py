from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserCreateForm, TeacherCreateForm, StudentCreateForm



from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# home
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
            return redirect('user:login')
    else:
        form = TeacherCreateForm()
    return render(request, 'registration/teacher_registration/registration.html', {'form': form})
# ---------------------------------------------------------


from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Course, Purchase,StudentDetials
from .forms import StudentDetailsForm,CourseForm


class success(LoginRequiredMixin, UpdateView):
    model = StudentDetials
    form_class = StudentDetailsForm
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context



def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("user:login")
        else:
            messages.error(request, 'Invalid username,email or password.')
    else:
        form = StudentCreateForm()
        
    return render(request, 'registration/signup.html', {'form': form})

# User login  student/teacher/staff/super_admin
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
                return redirect('teachers:tr-dahboard')
            elif user.is_student:
                return redirect('students:index')
            else:
                return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('user:index')




@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = request.user
    if Purchase.objects.filter(course=course, student=student).exists():
        messages.warning(request, 'You have already purchased this course.')
        return redirect('user:dashboard')
    if request.method == 'POST':
        purchase = Purchase(course=course, student=student)
        purchase.save()
        messages.success(request, 'Course purchased successfully!')
        return redirect('user:dashboard')
    return render(request, 'purchase.html', {'course': course})



# @login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
def dashboard(request):
    purchases = Purchase.objects.filter(student=request.user)
    return render(request, 'dashboard.html', {'purchases': purchases})