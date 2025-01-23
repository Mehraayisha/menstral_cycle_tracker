# tracker1/models.py
from django.db import models
from django.contrib.auth.models import User

class MenstrualCycle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='menstrual_cycle')
    last_period = models.DateField()
    cycle_length = models.IntegerField(help_text="Cycle length in days")
    period_duration = models.IntegerField(help_text="Duration of period in days")
    cycle_regular = models.BooleanField(help_text="Is the cycle regular?")
    
    def __str__(self):
        return f"{self.user.username}'s Menstrual Cycle" 