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
        
        context = {'form': form,
                    'teacher_details_exists': teacher_details_exists,
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
    