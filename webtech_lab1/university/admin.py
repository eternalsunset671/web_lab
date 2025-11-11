from django.contrib import admin
from .models import Student, Instructor, Course, Enrollment

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'specialization')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('specialization',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'faculty', 'is_active', 'created_at')
    list_filter = ('is_active', 'faculty')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'level', 'duration', 'is_active')
    list_filter = ('level', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'created_at')
    list_filter = ('status', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__title')
