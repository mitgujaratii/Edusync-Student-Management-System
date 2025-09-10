from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-student/', views.add_student_view, name='add_student'),
    path('student-log/', views.student_log_view, name='student_log'),
    path('update-student/<int:pk>/', views.update_student_view, name='update_student'),
    path('delete-student/<int:pk>/', views.delete_student_view, name='delete_student'),
    path('attendance-log/', views.attendance_log_view, name='attendance_log'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('', views.login_view, name='home'),
]
