from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
app_name='user'
urlpatterns = [
    path('home/',views.index,name="index"),
    path('user-create/',views.create_user,name="createuser"),
    path('teacher/',views.create_teacher,name="creatTeacher"),
    path('student/',views.create_student,name="creatStudent"),


    # include the login and logout views
     path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
