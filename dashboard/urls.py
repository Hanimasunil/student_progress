from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # root goes to login
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout, name='logout'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/update/<int:pk>/', views.update_student, name='update_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('progress/add/<int:student_id>/', views.add_progress, name='add_progress'),
]
