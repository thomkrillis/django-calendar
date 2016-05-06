from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Event

import datetime

def create_event(event_name, days):
    start_date = timezone.now() + datetime.timedelta(days=days)
    end_date = timezone.now() + datetime.timedelta(days=days+1)
    return Event.objects.create(event_name=event_name,
                                   start_date=start_date, end_date=end_date)

class EventViewTests(TestCase):
    def test_index_view_with_no_events(self):
        # There should be no events
        response = self.client.get(reverse('mycalendar:events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events coming up.")
        self.assertQuerysetEqual(response.context['event_list'], [])

    def test_index_view_with_a_future_event(self):
        # There should be one event
        create_event(event_name="Future event.", days=30)
        response = self.client.get(reverse('mycalendar:events'))
        self.assertQuerysetEqual(
            response.context['event_list'],
            ['<Event: Future event.>']
        )

    def test_index_view_with_a_past_event(self):
        # There should be no events
        create_event(event_name="Past event.", days=-30)
        response = self.client.get(reverse('mycalendar:events'))
        self.assertContains(response, "No events coming up.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['event_list'], [])

    def test_index_view_with_past_event_and_future_event(self):
        # There should be one event (the future event)
        create_event(event_name="Future event.", days=30)
        create_event(event_name="Past event.", days=-30)
        response = self.client.get(reverse('mycalendar:events'))
        self.assertQuerysetEqual(
            response.context['event_list'],
            ['<Event: Future event.>']
        )

    def test_index_view_with_two_future_events(self):
        # There should be two events
        create_event(event_name="Future event 1.", days=30)
        create_event(event_name="Future event 2.", days=5)
        response = self.client.get(reverse('mycalendar:events'))
        self.assertQuerysetEqual(
            response.context['event_list'],
            ['<Event: Future event 2.>', '<Event: Future event 1.>']
        )

class EditViewTests(TestCase):
    def test_edit_view_with_a_future_event(self):
        # Future event should be editable
        future_event = create_event(event_name='Future event.',
                                          days=5)
        response = self.client.get(reverse('mycalendar:edit',
                                   args=(future_event.id,)))
        self.assertContains(response, future_event.event_name,
                            status_code=200)

    def test_edit_view_with_a_past_event(self):
        # Past event should not be editable
        past_event = create_event(event_name='Past Event.',
                                        days=-5)
        response = self.client.get(reverse('mycalendar:edit',
                                   args=(past_event.id,)))
        self.assertEqual(response.status_code, 404)
