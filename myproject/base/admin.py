from django.contrib import admin
from .models import Course
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display=['id','course_name','course_code','is_delete']
    search_fields=('course_name','course_code')
    list_filter = ['is_delete']
    ordering = ('course_code',)


admin.site.register(Course,CourseAdmin)