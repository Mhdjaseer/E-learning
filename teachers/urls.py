from django.urls import path
from .import  views

app_name='teachers'

urlpatterns = [
    path('dashboard/',views.teacher_dashboard.as_view(),name='tr-dahboard'),
    path('profile/',views.Teacher_Profile.as_view(),name="teacher-profile"),
    path('courselist/',views.TeacherCourseList,name="course-list"),
    path('select/course/<int:course_id>/',views.teacherPurchaseCourse,name='selectCourse'),

    path('student/',views.Student_Course_Purchased_By_Teacher_Selected_Course.as_view(),name="student-purchased")
]
