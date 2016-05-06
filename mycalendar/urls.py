from django.conf.urls import url

from . import views

app_name = 'mycalendar'
urlpatterns = [
    url(r'^$', views.CalendarView.as_view(), name='events'),
    url(r'^new/$', views.NewView.as_view(), name='new'),
    url(r'^new/submitNew/$', views.submitNew, name='submitNew'),
    url(r'^(?P<pk>[0-9]+)/$', views.EditView.as_view(), name='edit'),
    url(r'^(?P<event_id>[0-9]+)/submitEdit/$', views.submitEdit, name='submitEdit'),
]
