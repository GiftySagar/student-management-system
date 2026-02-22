from django.shortcuts import render,redirect,get_object_or_404
from .models import Course,Student,CourseStudent
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request,'home.html')

def course_list(request):
    courses = Course.objects.filter(is_delete=False)
    enrollments=CourseStudent.objects.filter(is_delete=False)
    return render(request,'course_list.html',{
                  'data':courses,
                  'enrolled':enrollments
                  })




def enroll_list(request):
    a= CourseStudent.objects.select_related('student','course').filter(is_delete=False)
    return render(request,'enroll_list.html',{'data':a})



def enroll(request,pk):
    student = get_object_or_404(Student,user=request.user)
    print(student)
    course = get_object_or_404(Course,id=pk)

    if CourseStudent.objects.filter(student=student,course=course,is_delete=False).exists():
        messages.warning(request,'You Have Already Enrolled For The Course')
        return redirect('course_list')

    CourseStudent.objects.create(
        student = student,
        course = course
    )
    return redirect('enroll_list')

from django.shortcuts import render


def search(request):
    query = request.GET.get('q') 
    
    if query:
        
    
        results = Course.objects.filter(
            Q(course_name__icontains=query) | Q(course_code__icontains=query)
        ) #.distinct() 
    else:
        results = Course.objects.none() 
        
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)


def about(request):
    return render(request,'about.html')

@login_required
def update(request):
    user=request.user
    student=user.student

    if request.method == 'POST':
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')

        
        student.contact = request.POST.get('contact')

        if 'simage' in request.FILES:
            student.simage = request.FILES['simage']

        user.save()
        student.save()

        messages.success(request, "Profile updated successfully ✅")


        return redirect('profile') 

    return render(request, 'update.html')






        
    
    
    









        
    
    



def soft_delete_enroll(request, pk):
    enroll = get_object_or_404(CourseStudent, pk=pk)
    enroll.is_delete = True
    enroll.save()
    messages.success(request, "Enrollment Moved To Trash.")
    return redirect('enroll_list')

def enroll_trash_list(request):
    deleted_enrollments = CourseStudent.objects.filter(is_delete=True)
    return render(request, 'enroll_trash_list.html', {
        'deleted_enrollments': deleted_enrollments
    })


def permanent_delete_enroll(request, pk):
    enroll = get_object_or_404(CourseStudent, pk=pk,is_delete=True)
    enroll.delete()
    messages.success(request, "Enrollment Permanently Deleted.")
    return redirect('enroll_trash_list')


def restore(request,pk):
    enroll=get_object_or_404(CourseStudent,pk=pk,is_delete=True)

    if CourseStudent.objects.filter(
        student=enroll.student,
        course=enroll.course,
        is_delete=False
    ).exists():
             messages.error(request,'Enrollment Exists Already')
             return redirect('enroll_trash_list')

    enroll.is_delete=False
    enroll.save()
    messages.success(request,"Enrollment Restored Successfully")
    return redirect ('enroll_list')
