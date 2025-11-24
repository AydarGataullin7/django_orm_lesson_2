from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
import datetime
from datacenter.models import get_duration, format_duration
from django.shortcuts import get_object_or_404


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    return duration > datetime.timedelta(minutes=minutes)


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        entered_time = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)

        this_passcard_visits.append({
            'entered_at': entered_time.strftime('%d %B %Y г. %H:%M'),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit, minutes=60)
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
