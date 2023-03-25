from django.urls import path
from . import views
app_name='students'
urlpatterns = [
    path('',views.index.as_view(),name="index"),
    path('home',views.home.as_view(),name="home")

]
