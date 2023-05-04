from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,CreateView
from django.views import View
from user.models import Student,TeacherDetials,Course,Purchase
from .forms import StudentForm
from django.views.generic import TemplateView,FormView
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from user.forms import TeacherDetailsForm
from django.contrib.auth.decorators import login_required








# teacher dashboard view
class teacher_dashboard(LoginRequiredMixin, View):
    form_class = TeacherDetailsForm
    template_name = 'teacher_dashbord.html'
    # success_url = reverse_lazy('student-details')



    def get(self, request):
        form = self.form_class()
        teacher_details_exists = TeacherDetials.objects.filter(user=request.user).exists()
        teacher_purchased_course=Teacher_Course_Select.objects.filter(instructor=request.user)
        
        context = {'form': form,
                    'teacher_details_exists': teacher_details_exists,
                    'teacher_purchased_course':teacher_purchased_course,
                    }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        teacher_details_exists = TeacherDetials.objects.filter(user=request.user).exists()
        if form.is_valid():
            teacher_details = form.save(commit=False)
            teacher_details.user = request.user
            teacher_details.save()
            messages.success(request, 'Your details have been saved.')
            return render(request, self.template_name, {'form': form, 'teacher_details_exists': True})
        else:
            context = {'form': form, 'teacher_details_exists': teacher_details_exists}
            return render(request, self.template_name, context)

class Teacher_Profile(TemplateView):
    template_name='teacher_profile.html'


from user.models import Teacher_Course_Select
def TeacherCourseList(request):
    course=Course.objects.all()
    select_course=Teacher_Course_Select.objects.filter(instructor=request.user)
    context={
        'courses':course,
        'select_course': select_course
    }
    return render (request,'teacher_course_lists.html',context)
####################################################################

# teacher select the course and dashboard 
def teacherPurchaseCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    teacher = request.user
    print(teacher)
    teacher_course_select = Teacher_Course_Select.objects.filter(course=course, instructor=teacher).first()
    select_course = False
    if teacher_course_select is not None:
        select_course = True
        messages.warning(request, 'You have already selected this course')
        
    if request.method == 'POST':
        select_course = Teacher_Course_Select(course=course, instructor=teacher)
        select_course.save()
        messages.success(request, 'Course selected successfully!')
        return redirect('teachers:course-list')
    
    context={
        'course': course,
        'teacher_course_select': teacher_course_select,
        'select_course': select_course,
    }
    
    return render(request, 'cours_detials.html', context)



# course that student purchased by teacher
class Student_Course_Purchased_By_Teacher_Selected_Course(View):
    template_name='student_course_purchased_by_teacher_selected_course.html'

    def get(self,request):
        student_purchase_course=Purchase.objects.filter(course__instructor=request.user)
        context={
            'student_purchase_course':student_purchase_course,
        }
        return render (request,self.template_name,context)