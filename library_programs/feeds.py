from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from django.urls import reverse

class UpcomingEventsFeed(Feed):
    title = "Penticton Public Library"
    link = "/rss/"
    description = "Upcoming Programs"

    def items(self):
        from library_programs.event_base import EventBase
        ev = EventBase()
        rd = ev.next_month_events 
        return rd

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