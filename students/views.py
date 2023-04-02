from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from user.models import Student, StudentDetials
from .forms import StudentForm, StudentDetailsForm
from django.views.generic import TemplateView

class studentAccount(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'users-profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.student

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['student_details_form'] = StudentDetailsForm(self.request.POST, instance=self.request.user.student.studentdetials)
    #     else:
    #         context['student_details_form'] = StudentDetailsForm(instance=self.request.user.student.studentdetials)
    #     return context

    def form_valid(self, form):
        context = self.get_context_data()
        student_details_form = context['student_details_form']
        if student_details_form.is_valid():
            student_details_form.save()
        return super().form_valid(form)

# students dashboard view
class index(TemplateView):
    template_name = 'students_detials.html'

