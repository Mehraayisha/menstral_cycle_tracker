from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tracker1.models import MenstrualCycle # Import the MenstrualCycle model

def index(request):
    today = datetime.today().date()  # Get today's date
    current_hour = datetime.now().hour
    start_of_week = today - timedelta(days=today.weekday())  # Get the start of the current week (Monday)

    # Generate the list of dates for the current week (Monday to Sunday)
    week_dates = [(start_of_week + timedelta(days=i)) for i in range(7)]

    # Extract the names of the weekdays (Monday, Tuesday, etc.)
    week_names = [date.strftime("%A")[0] for date in week_dates]

    # Determine the greeting based on the time of day
    if 5 <= current_hour < 12:
        greeting = "Good Morning Sunshine"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening sweetheart"

    # Get the current day (number) from today's date
    current_day_number = today.day  # e.g., 19

    # Fetch or create the user's menstrual cycle information
    cycle_info = None
    if request.user.is_authenticated:  # Ensure the user is authenticated
        user = request.user
        if MenstrualCycle.objects.filter(user=user).exists():
            cycle_info = MenstrualCycle.objects.get(user=user)
    
    # Pass the variables to the template
    return render(request, "index.html", {
        'greeting': greeting,
        'week_names': week_names,
        'week_dates': week_dates,  # Pass the full date objects
        'today': today,
        'current_day_number': current_day_number,  # Pass the day number to highlight
        'cycle_info': cycle_info,  # Pass the cycle_info (None if not filled out yet)
    })
@login_required  # Ensure the user is logged in
def cycle_details(request):
    if request.method == 'POST':
        # Collect menstrual cycle details from the POST request
        last_period = request.POST.get('last_period')
        cycle_length = request.POST.get('cycle_length')
        period_duration = request.POST.get('period_duration')
        cycle_regular = request.POST.get('cycle_regular') == 'on'  # Handle checkbox (True/False)

        # Get or create a MenstrualCycle record for the logged-in user
        user = request.user
        cycle_info, created = MenstrualCycle.objects.get_or_create(user=user)

        # Update the cycle info
        cycle_info.last_period = last_period
        cycle_info.cycle_length = cycle_length
        cycle_info.period_duration = period_duration
        cycle_info.cycle_regular = cycle_regular
        cycle_info.save()

        # Display success message
        messages.success(request, 'Cycle details have been saved successfully!')
        return redirect('home')  # Redirect to home page after saving the details

    return render(request, 'details.html')  
