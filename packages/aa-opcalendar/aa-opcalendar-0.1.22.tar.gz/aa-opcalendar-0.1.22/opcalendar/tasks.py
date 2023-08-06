from celery import shared_task
import datetime
import feedparser
import logging
from .models import Event, EventImport

logger = logging.getLogger(__name__)

# Import eve uni classes
@shared_task
def import_fleets():
	
	#Clear out all fleets to remove deleted fleets
	Event.objects.filter(visibility="import").delete()

	#Get all import feeds
	feeds = EventImport.objects.all()
	
	for feed in feeds:
		if feed.source=="Spectre Fleet":

			#Get fleets from SF RSS
			d = feedparser.parse('https://www.spectre-fleet.space/engagement/events/rss')
			for entry in d.entries:
				##Look for SF fleets only
				if entry.author_detail.name=='Spectre Fleet':
					#Only active fleets
					if not "[RESERVED]" in entry.title:

						date_object = datetime.datetime.strptime(entry.published,'%a, %d %b %Y %H:%M:%S %z')
						date_object.strftime('%Y-%m-%dT%H:%M')

						event = Event(
							operation_type=feed.operation_type,
							title=entry.title,
							host=feed.host,
							doctrine="",
							formup_system="",
							description=entry.description,
							start_time=date_object, 
							end_time=date_object, 
							fc="",
							visibility="import",
							user_id=1
						)
						event.save()

@shared_task
def add(x, y):
    return x + y

   