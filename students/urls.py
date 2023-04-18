from django.urls import path
from . import views
app_name='students'
urlpatterns = [
    path('index',views.index.as_view(),name="index"),
    path('account/',views.studentAccount.as_view(),name="stuedentAccount"),
    path('couses/',views.students_course_purchase.as_view(),name="courses"),
    path('coursepurchase/<int:course_id>/',views.purchase_course,name='purchase')
]
