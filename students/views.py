from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,CreateView
from django.views import View
from user.models import Student,StudentDetials
from .forms import StudentForm
from django.views.generic import TemplateView,FormView
from django.contrib import messages
from django.shortcuts import render,redirect

class studentAccount(LoginRequiredMixin, UpdateView):
    model = Student,StudentDetials
    form_class = StudentForm
    template_name = 'users-profile.html'
    success_url = reverse_lazy('students:index')

    def get_object(self, queryset=None):
        return self.request.user.student
    


    def form_valid(self, form):
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')

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
from user.forms import StudentDetailsForm
from django.contrib.auth.decorators import login_required

# @login_required
# def index(request):
#     if request.method == 'POST':
#         form = StudentDetailsForm(request.POST, request.FILES)
#         try:
#             student_details_exists=StudentDetials.objects.filter(user=request.user).exists()
#             if student_details_exists :
#                     print("yes its exists ",student_details_exists)
#                     messages.error(request,'Data is already exists')
#                         # redirect to a success page or something
#         except:
#                 if form.is_valid():
#                     student_details = form.save(commit=False)
#                     student_details.user = request.user
    
#                     student_details.save()
#                     messages.success(request,'Data is entered success fully ')
#     else:
#         form = StudentDetailsForm()
    
 

    
#     return render(request, 'students_detials.html', {'form': form})


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