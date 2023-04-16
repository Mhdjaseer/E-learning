from django.urls import path
from . import views
app_name='students'
urlpatterns = [
    path('index',views.index.as_view(),name="index"),
    path('account/',views.studentAccount.as_view(),name="stuedentAccount"),
    path('purchase/',views.students_course_purchase.as_view(),name="purchase"),
]
