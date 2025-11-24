from datacenter.models import Visit
from datacenter.models import get_duration, format_duration
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at__isnull=True)

    non_closed_visits = []

    for visit in active_visits:

        entered_time = timezone.localtime(visit.entered_at)

        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        formatted_entered_time = entered_time.strftime('%d %B %Y г. %H:%M')

        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': formatted_entered_time,
            'duration': formatted_duration,
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
