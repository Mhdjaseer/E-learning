from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.views.generic import TemplateView

app_name='user'
urlpatterns = [
    path('index/',views.index,name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"),name="about"),
    path("teachers/",views.teachers.as_view(),name="teachers"),
    path("contact/",views.contact.as_view(),name="contact"),



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

    # teacher select the course
    # path('select/course/<int:course_id>/',views.teacherPurchaseCourse,name='selectCourse'),
    path('teachercourselist',views.TeacherCourseList,name='teachercourselist'),

    # otp
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),


    # forgotpassword
    path('forgot-password/',views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/',views.VerifyOtpView.as_view(), name='verify_otp'),
    path('reset-password/',views.ResetPasswordView.as_view(), name='reset_password'),

]
