from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from base.models import Student
from django.contrib.auth.decorators import login_required








# Create your views here.
def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(username=username,password=password)
        if u:
            login(request,u)
            return redirect('home')
        else:
            messages.error(request,"Invalid Username Or Password")
            

    return render(request,'login_.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        simage = request.FILES.get('simage')
        contact=request.POST['contact']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        
        
        user= User.objects.create(
            first_name = fname,
            last_name= lname,
            email = email,
            username = username,
            
        )
        user.set_password(password)
        user.save()

        Student.objects.create(
            user=user,
            first_name=fname,
            last_name=lname,
            email=email,
            simage=simage,
            contact=contact  
        )
        messages.success(request, 'Registration successful')
        return redirect('login_')
    return render(request,'register.html')




def logout_(request):
    logout(request)
    return redirect('login_')

@login_required
def profile(request):
    student = Student.objects.get(user=request.user)


    if request.method=="POST":
        if request.FILES.get('simage'):
            student.simage=request.FILES['simage']
            student.save()


    return render(request,'profile.html',{'student':student})


def reset(request):
    u = User.objects.get(username=request.user)#fletch the data from the database
    if request.method == 'POST':
        try: 
            old_pasw = request.POST['oldpasw']#fletch the data from the frontend side 
            u = authenticate(username=u.username,password = old_pasw)#check the username and password enterd by the user
            if u:
                return render(request,'reset.html',{'newpass':True}) 
            else:
                return render(request,'reset.html',{'wrong':True})
        except:
            new_pasw = request.POST['newpasw']
            u.set_password(new_pasw)
            u.save()
            return redirect('login_')
    return render(request,'reset.html')

#get method - error
# old password -wrong

def forgot_password(request):
    if request.method == 'POST':
        # username = request.POST['username']
        username = request.POST.get('username')#fletched the data from frontend side
        # print(request.POST)
        try:
            u =  User.objects.get(username=username)#fletched the data from the database
            request.session['fp_user'] = u.username#store the usename in the session storage
            return redirect('new_password')

        except User.DoesNotExist:
            return render(request,'forgot_password.html',{'error':'The username not found......!!!'})
    return render(request,'forgot_password.html')


def new_password(request):
    username = request.session.get('fp_user')#fletching data from the session storage

    if username is None:
        return redirect('forgot_password')
    
    u =  User.objects.get(username=username)#fletching the data from the database
    if request.method == 'POST':
        new_pass = request.POST.get('password')
        u.set_password(new_pass)
        u.save()
        return redirect('login_')

    return render(request,'new_password.html')





