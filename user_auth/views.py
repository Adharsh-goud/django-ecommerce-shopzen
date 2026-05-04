from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import CartModel

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login_')
    
    return render(request,'register.html',{
        'page_type': 'auth'
    })

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login_')

    return render(request,'login_.html',{
        'page_type': 'auth'
    })

@login_required(login_url='login_')
def profile(request):
    cartproducts_count = CartModel.objects.filter(host = request.user).count()
    if not request.user.is_authenticated:
        return redirect('login_')
    return render(request,'profile.html', {'cartproducts_count':cartproducts_count})

def logout_(request):
    logout(request)
    return redirect('login_')

def reset_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_password = request.POST.get('new_password',{
            'page_type': 'auth'
        })

        try:
            user = User.objects.get(username=username)

            if user.check_password(new_password):
                messages.error(request, "New password cannot be same as old password")
                return redirect('reset_password')

            user.set_password(new_password)
            user.save()

            messages.success(request, "Password reset successful")
            return redirect('login_')

        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('reset_password')

    return render(request, 'reset_password.html',{
        'page_type': 'auth'
    })

def update_profile(request):
    data = request.user #user object
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        data.first_name = fname
        data.last_name = lname
        data.email = email
        data.save()
        return redirect('profile')

    return render(request,'update_profile.html',{
        'page_type': 'auth'
    })

'''
1.register
2.login_
3.profile
4.logout_
5.reset password
6.forgot password

'''