from django.urls import path
from library_programs import views

urlpatterns = [
    path('library_programs/calendar_feed.ics', views.event_feed_view, name='calendar_feed'),
]