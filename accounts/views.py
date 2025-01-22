from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import auth
from django.core.exceptions import ValidationError
# Logout view
def logout(request):
    auth.logout(request)
    messages.success(request,'logged out successfully')
    return redirect('login')  # Redirect to the login page after logging out

# Login view
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)

            return redirect('/') # Redirect to home page or any other page
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Stay on the login page if authentication fails

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        

        # Create the user if everything is valid
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.save()

        # Log the user in after successful signup
        auth_login(request, user)

        # Redirect to the details page (cycle details collection page)
        messages.success(request, 'User created successfully. Please complete your cycle details.')
        return redirect('cycle_details')  # Redirect to cycle details page after signup

    return render(request, 'signup.html')