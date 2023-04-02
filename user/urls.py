from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
app_name='user'
urlpatterns = [
    path('index/',views.index,name="index"),
    path('user-create/',views.create_user,name="createuser"),
    path('teacher/',views.create_teacher,name="creatTeacher"),
    path('student-create/',views.create_student,name="creatStudent"),#student registration 


    path('student-success/',views.success.as_view(),name="success"),#after login the page have profile and the courselist 


    path('courses/<int:course_id>/purchase/',views.purchase_course, name='purchase_course'),#course purchasing linkk 
    path('course-create/',views.create_course,name="cours_Create"),#course create only the super-admin or the staff can only 

     path('dashboard/', views.dashboard, name='dashboard'),#this is the dashboard that helps to display the student purchased course in the dashboard 

    # include the login and logout views
     path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
