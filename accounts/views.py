from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth
from django.core.exceptions import ValidationError

# Logout view
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('signinup')  # Redirect to the login page after logging out

# Login and Signup view (both in the same page)
def signinup(request):
    if request.method == "POST":
        # Handle login
        if 'signin_submit' in request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')  # Redirect to home page or any other page
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('signinup')  # Stay on the page if login fails

        # Handle signup
        elif 'signup_submit' in request.POST:
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('signinup')

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signinup')

            # Create the user if everything is valid
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()

            # Log the user in after successful signup
            auth_login(request, user)

            # Redirect to the home page after successful signup
            return redirect('home')

    return render(request, 'signinup.html')
