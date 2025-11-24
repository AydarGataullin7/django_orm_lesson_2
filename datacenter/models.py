from django.db import models
from django.utils import timezone
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    if visit.leaved_at:
        leaved_time = timezone.localtime(visit.leaved_at)
        entered_time = timezone.localtime(visit.entered_at)
        return leaved_time - entered_time
    else:
        current_time = timezone.localtime()
        entered_time = timezone.localtime(visit.entered_at)
        return current_time - entered_time


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    seconds_in_hour = 3600
    seconds_in_minute = 60
    hours = total_seconds // seconds_in_hour
    minutes = (total_seconds % seconds_in_hour) // seconds_in_minute
    return f"{hours:02d}:{minutes:02d}"
