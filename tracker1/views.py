from django.shortcuts import render
from datetime import datetime, timedelta

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
        greeting = "Good Evening sweatheart"

    # Get the current day (number) from today's date
    current_day_number = today.day  # e.g., 19

    # Pass the variables to the template
    return render(request, "index.html", {
        'greeting': greeting,
        'week_names': week_names,
        'week_dates': week_dates,  # Pass the full date objects
        'today': today,
        'current_day_number': current_day_number,  # Pass the day number to highlight
    })
