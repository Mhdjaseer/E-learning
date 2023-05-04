from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserCreateForm, TeacherCreateForm, StudentCreateForm

from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Course, Purchase,StudentDetials,Teacher_Course_Select,Teacher
from .forms import StudentDetailsForm,CourseForm

import random

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

# ---------------------------------------------------------



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

from django.conf import settings
from twilio.rest import Client
from .models import User, Student



def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP for registration is {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                # to=user.phone_number
                to='+918137974704'
            )
            return redirect('user:verify_otp', user_id=user.id)
        else:
            print(form.errors)
            messages.error(request, 'Invalid username, email or password.')
    else:
        form = StudentCreateForm()
        
    return render(request, 'registration/signup.html', {'form': form})


def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP for registration is {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                # to=user.phone_number
                to='+918137974704'
            )
            return redirect('user:verify_otp', user_id=user.id)
        else:
            print(form.errors)
            messages.error(request, 'Invalid username, email or password.')
    else:
        form = TeacherCreateForm()
    return render(request, 'registration/teacher_registration/registration.html', {'form': form})


def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == user.otp:
            
            user.is_active = True
            user.save()
            # student = Student(user=user)
            # student.save()
            return redirect('user:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'registration/verify_otp.html')



# User login  student/teacher/staff/super_admin
def user_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        
        user = authenticate(request,phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            elif user.is_teacher:
                print(' yes it is teacher ')
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

# #########################################################
# teacher select the course and dashboard 
# def teacherPurchaseCourse(request, course_id):
#     course = get_object_or_404(Course, pk=course_id)
#     teacher=request.user
#     teacher_course_select = Teacher_Course_Select.objects.filter(course=course, instructor=teacher).first()
#     if teacher_course_select is not None:
#         messages.warning(request, 'You have already selected this course')
#         return redirect('user:teachercourselist')

#     if request.method == 'POST':
#         select_course = Teacher_Course_Select(course=course, instructor=teacher)
#         select_course.save()
#         messages.success(request, 'Course selected successfully!')
#         return redirect('user:teachercourselist')
#     return render(request, 'teacher_course_select.html', {'course': course})

# dlt 
def TeacherCourseList(request):
    course=Course.objects.all()
    select_course=Teacher_Course_Select.objects.filter(instructor=request.user)
    context={
        'courses':course,
        'select_course': select_course
    }
    return render (request,'teacher_course_list.html',context)
#######################################################################
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


# teachers home page and search the teachers--- also need to change the count number 
class teachers(TemplateView):
    template_name = 'teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all()
        context["teachers"] = random.sample(list(teachers), 2)#need to change the count number 
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        search_term = request.POST.get('search', '').strip()
        if search_term:
            teachers = Teacher.objects.filter(first_name__icontains=search_term)
            context['teachers'] = teachers
            
        return self.render_to_response(context)
# contact page

class contact(TemplateView):
    template_name = 'contact.html'





# forgot password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
User = get_user_model()

class ForgotPasswordView(View):
    template_name = 'registration/password_rest/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this phone number')
            return redirect(reverse('user:forgot_password'))

        otp = random.randint(1000, 9999)
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            # to=phone_number,
            to='+918137974704',
            from_=settings.TWILIO_PHONE_NUMBER,
            body=f"Your OTP for resetting the password is {otp}"
        )
        request.session['phone_number'] = phone_number
        request.session['otp'] = otp
        return redirect(reverse_lazy('user:verify_otp'))


class VerifyOtpView(View):
    template_name = 'registration/password_rest/verify_otp.html'

    def get(self, request):
        if 'phone_number' not in request.session or 'otp' not in request.session:
            messages.error(request, 'OTP session expired')
            return redirect(reverse_lazy('user:forgot_password'))
        return render(request, self.template_name)

    def post(self, request):
        if 'phone_number' not in request.session or 'otp' not in request.session:
            messages.error(request, 'OTP session expired')
            return redirect(reverse_lazy('user:forgot_password'))

        phone_number = request.session['phone_number']
        user = User.objects.get(phone_number=phone_number)
        otp = request.session['otp']
        entered_otp = request.POST.get('otp')
        if int(entered_otp) != otp:
            messages.error(request, 'Invalid OTP')
            return redirect(reverse_lazy('verify_otp'))
        request.session.pop('phone_number')
        request.session.pop('otp')
        request.session['reset_user_id'] = user.pk
        return redirect(reverse_lazy('user:reset_password'))



class ResetPasswordView(View):
    template_name = 'registration/password_rest/reset_password.html'

    def get(self, request):
        if 'reset_user_id' not in request.session:
            messages.error(request, 'Invalid session')
            return redirect(reverse_lazy('user:forgot_password'))
        return render(request, self.template_name)

    def post(self, request):
        if 'reset_user_id' not in request.session:
            messages.error(request, 'Invalid session')
            return redirect(reverse_lazy('user:forgot_password'))

        user = User.objects.get(pk=request.session['reset_user_id'])
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect(reverse_lazy('user:reset_password'))

        try:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect(reverse_lazy('user:login'))
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect(reverse_lazy('user:reset_password'))