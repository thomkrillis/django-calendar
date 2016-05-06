from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Event

import sys
import datetime

class CalendarView(generic.ListView):
    template_name = 'mycalendar/index.html'

    def get_queryset(self):
        return Event.objects.filter(end_date__gte=timezone.now()).order_by('start_date')

class NewView(generic.TemplateView):
    template_name = 'mycalendar/new.html'

def submitNew(request):
    try:
        event = Event(event_name=request.POST['name'],start_date=datetime.datetime.strptime(request.POST['start-date'] + request.POST['start-time'], '%Y-%m-%d%H:%M'),end_date=datetime.datetime.strptime(request.POST['end-date'] + request.POST['end-time'], '%Y-%m-%d%H:%M'))
    except ValueError:
        return render(request, 'mycalendar/new.html', {
            'error_message': "The provided data was not valid.",
        })
    try:
        event.save()
    except ValidationError:
        # Redisplay the new event form.
        return render(request, 'mycalendar/new.html', {
            'error_message': "The provided data was not valid.",
        })
    else:
        return HttpResponseRedirect(reverse('mycalendar:events'))

class EditView(generic.DetailView):
    model = Event
    template_name = 'mycalendar/edit.html'

    def get_queryset(self):
        return Event.objects.filter(end_date__gte=timezone.now())

def submitEdit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.event_name = request.POST['name']
    try:
        event.start_date = datetime.datetime.strptime(request.POST['start-date'] + request.POST['start-time'], '%Y-%m-%d%H:%M')
        event.end_date = datetime.datetime.strptime(request.POST['end-date'] + request.POST['end-time'], '%Y-%m-%d%H:%M')
    except ValueError:
        return render(request, 'mycalendar/edit.html', {
            'event': event,
            'error_message': "The provided data was not valid.",
        })
    try:
        event.save()
    except ValidationError:
        # Redisplay the event edit form.
        return render(request, 'mycalendar/edit.html', {
            'event': event,
            'error_message': "The provided data was not valid.",
        })
    else:
        return HttpResponseRedirect(reverse('mycalendar:events'))
