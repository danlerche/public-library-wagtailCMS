from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from django.urls import reverse
from library_programs.models import Event
import datetime

class UpcomingEventsFeed(Feed):
    title = "Penticton Public Library"
    link = "/rss/"
    description = "Upcoming Programs"

    def items(self):
        today = datetime.datetime.now()
        next_month_events = []
        events_qs = Event.objects.live()
        thirty_days = today + datetime.timedelta(30)
        s_events_qs = Event.objects.filter(repeats__isnull=True).live()
        r_events_qs = Event.objects.filter(repeats__isnull=False).live()
        from library_programs.event_base import EventQueries
        eq = EventQueries()
        all_events = eq.all_events(s_events_qs, r_events_qs)
        for event_index in range(len(all_events)):
            event_dates = all_events[event_index]['event_date']
            if all_events[event_index]['event_date'] >= today and all_events[event_index]['event_date'] <= thirty_days:
                next_month_events.append(all_events[event_index])
        return next_month_events

    def item_title(self, item):
        return item['title']

    def item_pubdate(self, item):
        return item['event_date']

    def item_description(self, item):
        return strip_tags(item['description'])

    def item_link(self, item):
        return item['url']

class AtomSiteNewsFeed(UpcomingEventsFeed):
    feed_type = Atom1Feed
    subtitle = UpcomingEventsFeed.description