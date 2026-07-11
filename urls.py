# onlinecourse/urls.py
from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # ... your existing paths (like index, login, logout, etc.) ...
    
    # Path for submitting the exam
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path for showing exam result
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
