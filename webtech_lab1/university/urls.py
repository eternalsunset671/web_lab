from django.urls import path
from . import views

# TODO
# пофиксить страницы студентов
 
urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('about/', views.AboutView.as_view(), name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    
    path('feedback/', views.feedback_view, name='feedback'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact')
]
