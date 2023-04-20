from django.urls import path
from .import  views

app_name='teachers'

urlpatterns = [
    path('dashboard/',views.teacher_dashboard.as_view(),name='tr-dahboard'),
]
