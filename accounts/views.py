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
    errors = {}
    form_type = "signin"  # Default to sign-in

    if request.method == "POST":
        # Handle login
        if 'signin_submit' in request.POST:
            form_type = "signin"
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')  # Redirect to home page
            else:
                errors['general'] = 'Invalid username or password'

        # Handle signup
        elif 'signup_submit' in request.POST:
            form_type = "signup"
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if password1 != password2:
                errors['password2'] = 'Passwords do not match'

            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username already exists'

            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email already registered'

            if not errors:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                auth_login(request, user)
                return redirect('home')

    return render(request, 'signinup.html', {'errors': errors, 'form_type': form_type})
