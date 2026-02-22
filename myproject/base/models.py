from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=20)
    course_code = models.IntegerField()
    is_delete = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    contact = models.IntegerField()
    address = models.TextField(max_length=100)
    branch = models.CharField(max_length=25)
    is_delete = models.BooleanField(default=False)
    simage = models.ImageField(upload_to='uploads/',default='Default.jpg',null=True,blank=True)


class CourseStudent(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    


    

