from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView
from django.urls import path
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('student/<int:pk>/', views.student_profile, name='student'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    
    path('feedback/', views.feedback_view, name='feedback'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('students/', views.student_list, name='students'),
    path('enroll/', views.enroll_view, name='enroll'),
    path('success/', views.success_view, name='success'),

    path('instructors/', views.InstructorListView.as_view(), name='instructor_list'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/course/<int:course_id>/', views.manage_course, name='manage_course'),
    path('set_grade/<int:enrollment_id>/', views.set_grade, name='set_grade'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    re_path(r'^accounts/login/$', RedirectView.as_view(url='/login/')),
]
