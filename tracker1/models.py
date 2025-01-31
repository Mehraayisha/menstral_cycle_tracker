# tracker1/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class MenstrualCycle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='menstrual_cycle')
    last_period = models.DateField()
    cycle_length = models.IntegerField(help_text="Cycle length in days")
    period_duration = models.IntegerField(help_text="Duration of period in days")
    cycle_regular = models.BooleanField(help_text="Is the cycle regular?")
    
    def __str__(self):
        return f"{self.user.username}'s Menstrual Cycle" 
    def get_days_passed(self):
        """
        Calculates the number of days passed in the current cycle.
        """
        today = date.today()
        days_since_last_period = (today - self.last_period).days
        return days_since_last_period

    def get_progress_percentage(self):
        """
        Calculates the percentage of the current cycle that has passed.
        """
        days_passed = self.get_days_passed()
        return (days_passed / self.cycle_length) * 100 if self.cycle_length else 0
    
    def get_period_end_date(self):
        """
        Returns the expected end date of the period based on the last period and duration.
        """
        return self.last_period + timedelta(days=self.period_duration)
    
    def is_in_period(self):
        """
        Checks if today is within the user's period.
        """
        period_end_date = self.get_period_end_date()
        today = date.today()
        return self.last_period <= today <= period_end_date