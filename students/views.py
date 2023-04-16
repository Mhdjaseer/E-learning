from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,CreateView
from django.views import View
from user.models import Student,StudentDetials,Course,Purchase
from .forms import StudentForm
from django.views.generic import TemplateView,FormView
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from user.forms import StudentDetailsForm

# students accountprofile view
class studentAccount(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'users-profile.html'
    success_url = reverse_lazy('students:index')

    

    def get_object(self, queryset=None):
        return self.request.user.student
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        student_details = StudentDetials.objects.filter(user=user).first()
        if self.request.method == 'POST':
            student_details_form = StudentDetailsForm(self.request.POST, self.request.FILES, instance=student_details)
            if student_details_form.is_valid():
                student_details_form.save()
                messages.success(self.request, 'Your student details have been updated successfully.')
            else:
                messages.error(self.request, 'There was an error updating your student details. Please try again.')
        else:
            student_details_form = StudentDetailsForm(instance=student_details)
        context['student_details'] = student_details
        context['student_details_form'] = student_details_form
        return context



    def form_valid(self, form):
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        # address=self.request.POST.get('address')

        # self.object.address=address
        self.object.first_name = first_name
        self.object.last_name = last_name

        self.object.save()
        messages.success(self.request, 'Your profile has been updated successfully.')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field_name, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field_name}: {error}')
        return super().form_invalid(form)


# students dashboard view
class index(LoginRequiredMixin, View):
    form_class = StudentDetailsForm
    template_name = 'students_detials.html'
    success_url = reverse_lazy('student-details')

    def get(self, request):
        form = self.form_class()
        student_details_exists = StudentDetials.objects.filter(user=request.user).exists()
        context = {'form': form, 'student_details_exists': student_details_exists}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        student_details_exists = StudentDetials.objects.filter(user=request.user).exists()
        if form.is_valid():
            student_details = form.save(commit=False)
            student_details.user = request.user
            student_details.save()
            messages.success(request, 'Your details have been saved.')
            return render(request, self.template_name, {'form': form, 'student_details_exists': True})
        else:
            context = {'form': form, 'student_details_exists': student_details_exists}
            return render(request, self.template_name, context)
        
#student course view and purchase
class students_course_purchase(TemplateView):
    template_name='students_course_purchase.html'

    # def get(self,request,course_id):
    #     course=get_object_or_404(Course,pk=course_id)
    #     student=request.user
    #     if Purchase.objects.filter(course=course,student=student).exists():
    #         print("you have already purchased")
    #         # return redirect('students:course')
    #     if request.method=='POST':
    #         purchase=Purchase(course=course,student=student)
    #         purchase.save()
    #         print("successfully purchased")
    #         # return redirect ('students:dashbord)
    #         context={
    #             'course':course
    #         }
    #     return render(request,'students_course_purchase.html',context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context