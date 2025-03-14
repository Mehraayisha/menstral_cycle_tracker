from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tracker1.models import MenstrualCycle # Import the MenstrualCycle model
#by sherin

#------
def home(request):
    return render(request, 'home.html') 

def login_redirect(request):
    return redirect('signinup')

def products(request):
    return render(request, 'products.html')
def video(request):
    return render(request, 'video.html')

@login_required
def tracking(request):
    today = datetime.today().date()  # Get today's date
    current_hour = datetime.now().hour
    start_of_week = today - timedelta(days=today.weekday())  # Get the start of the current week (Monday)

    # Generate the list of dates for the current week (Monday to Sunday)
    week_dates = [(start_of_week + timedelta(days=i)) for i in range(7)]

    # Extract the names of the weekdays (Monday, Tuesday, etc.)
    week_names = [date.strftime("%A")[0] for date in week_dates]

    # Determine the greeting based on the time of day
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # Get the current day (number) from today's date
    current_day_number = today.day  # e.g., 19

    # Fetch the user's menstrual cycle information
    cycle_info = None
    period_dates = []
    period_data = None
    if request.user.is_authenticated:  # Ensure the user is authenticated
        user = request.user
        if MenstrualCycle.objects.filter(user=user).exists():
            cycle_info = MenstrualCycle.objects.get(user=user)
             # Calculate the start and end date of the user's period
            last_period_date = cycle_info.last_period
            cycle_length = cycle_info.cycle_length
            period_duration = cycle_info.period_duration

            # Predict next period dates
            next_period_start, next_period_end = predict_next_period(last_period_date, cycle_length, period_duration)

            # Check if the period overlaps with the current week
            period_dates = []
            for i in range(period_duration):
                period_day = next_period_start + timedelta(days=i)
                if period_day <= today and period_day in week_dates:
                    period_dates.append(period_day)

            period_data = get_period_progress(last_period_date, cycle_length, period_duration)
       
    
    # Pass the variables to the template
    return render(request, "tracking.html", {
        'greeting': greeting,
        'week_names': week_names,
        'week_dates': week_dates,  # Pass the full date objects
        'today': today,
        'current_day_number': current_day_number,  # Pass the day number to highlight
        'cycle_info': cycle_info,
        'period_dates': period_dates ,
         'period_data': period_data, # Pass the list of period dates
    })



@login_required  # Ensure the user is logged in before accessing this view
def tracker(request):
    # Check if the user has already entered their menstrual cycle details
    user = request.user
    if MenstrualCycle.objects.filter(user=user).exists():
        # If the details are already entered, redirect to the index page
        messages.info(request, "Your cycle details are already saved.")
        return redirect('tracking')  # or you can redirect to any other page like home
    else:
        # If no details are saved, show the details form
        return render(request, 'details.html')


def predict_next_period(last_period, cycle_length, period_duration):
    """
    Predict the next period based on the last period date, cycle length, and period duration.
    
    :param last_period: The date the last period started (datetime object)
    :param cycle_length: The cycle length (in days)
    :param period_duration: The period duration (in days)
    :return: A tuple with the predicted start and end dates of the next period.
    """
    # Ensure last_period is a datetime object
    if isinstance(last_period, str):
        last_period = datetime.strptime(last_period, "%Y-%m-%d")  # Convert string to datetime if needed

    # Predict the start date of the next period (add cycle_length days to the last period)
    next_period_start = last_period + timedelta(days=cycle_length)
    
    # Predict the end date of the next period (add period_duration days to the start date)
    next_period_end = next_period_start + timedelta(days=period_duration)

    return next_period_start, next_period_end



@login_required  # Ensure the user is logged in
def cycle_details(request):
    user = request.user

    # Check if the user already has menstrual cycle details
    try:
        cycle_info = MenstrualCycle.objects.get(user=user)
        return redirect('tracking')

    except MenstrualCycle.DoesNotExist:
        cycle_info = None  # User doesn't have details, so we can collect them

    if request.method == 'POST':
        # Collect menstrual cycle details from the POST request
        last_period = request.POST.get('last_period')
        cycle_length = request.POST.get('cycle_length')
        period_duration = request.POST.get('period_duration')
        cycle_regular = request.POST.get('cycle_regular') == 'on'  # Handle checkbox (True/False)

        # If the user doesn't have menstrual cycle details, create a new record
        if cycle_info is None:
            cycle_info = MenstrualCycle(user=user)

        # Update the cycle info
        cycle_info.last_period = last_period
        cycle_info.cycle_length = cycle_length
        cycle_info.period_duration = period_duration
        cycle_info.cycle_regular = cycle_regular
        cycle_info.save()

        # Display success message
        messages.success(request, 'Cycle details have been saved successfully!')
        return redirect('tracking')  # Redirect to home page after saving the details

    return render(request, 'details.html', {'cycle_info': cycle_info})  # Render the details page


def get_period_progress(last_period_date, cycle_length, period_duration):
    today = datetime.today().date()
    # Calculate the start and end of the current period
    next_period_start, next_period_end = predict_next_period(last_period_date, cycle_length, period_duration)

    if next_period_start <= today <= next_period_end:
        # User is on their period, calculate the progress and the day of the period
        days_into_period = (today - next_period_start).days + 1  # +1 because the period starts on the first day
        progress = (days_into_period / period_duration) * 100
        return {
            'on_period': True,
            'progress': round(progress, 2),
            'day_of_period': days_into_period,  # The current day of the period
            'period_duration': period_duration,  # The total length of the period
            'days_left': None ,
            'period_days': [next_period_start + timedelta(days=i) for i in range(days_into_period)] # No need to show days left if on period
        }
    else:
        # User is not on their period, calculate days until next period
        days_until_next_period = (next_period_start - today).days
        if days_until_next_period < 0:
            # In case there's a mistake with the dates, fallback to zero days
            days_until_next_period = 0
        return {
            'on_period': False,
            'progress': 0,
            'day_of_period': None,
            'period_duration': None,
            'days_left': days_until_next_period,
            'period_days': []
        }
