from django.views.generic import ListView,FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import Student
from .forms import UserProfileForm,studentdetials

class index(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students_dashbord.html"
    success_url = reverse_lazy('students:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm(initial={
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
        })
        context['student_form'] = studentdetials()
        return context


    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        student_form = studentdetials(request.POST)
        if form.is_valid() and student_form.is_valid():
            student_form.save()
            form.save()
            student_instance = student_form.save(commit=False)
            student_instance.user = request.user
            student_instance.save()
            return redirect('students:index')
        else:
            return self.get(request, *args, **kwargs)

from user.models import StudentDetials

class home(FormView):
    template_name = 'students_detials.html'
    form_class = studentdetials
    success_url = '/success/'  # Replace with your desired success URL

    def form_valid(self, form):
        # Get the user profile for the current user
        
        user_profile = self.request.user.email
        print(user_profile)
        # Create a new student details object and assign the user profile
        student_details = form.save(commit=False)
        student_details.profile_id = user_profile

        # Save the student details object to the database
        student_details.save()

        return super().form_valid(form)