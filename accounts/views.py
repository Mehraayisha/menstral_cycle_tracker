from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
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

# Signup view
def signup(request):
    if request.method == 'POST':
        
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        # Create the user if everything is valid
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Display success message and redirect to login page
        messages.success(request, 'User created successfully. Please login.')
        return redirect('login')  # Redirect to login page after successful signup

    # If it's a GET request, render the signup page
    return render(request, 'signup.html')
