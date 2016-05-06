from __future__ import unicode_literals

from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        return self.event_name
