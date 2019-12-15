from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('studentinfo/', views.studentinfo, name = 'studentinfo'),
    path('courseinfo/', views.courseinfo, name = 'courseinfo'),
    path('studentEnrollment/', views.studentEnrollment, name = 'studentEnrollment'),
    path('studentgraduate/', views.graduationRate, name = 'studentgraduate')

]

