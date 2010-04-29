import urllib
import urllib2

from google.appengine.ext import db
from google.appengine.ext import webapp
import wsgiref.handlers
import twitter
import twitterhelper as th
import twitterhelper as th
from google.appengine.ext.webapp import template
from google.appengine.api import mail
import os
import datetime

import httplib # used for talking to the Fire Eagle server
import oauth # the lib you downloaded

SERVER = 'fireeagle.yahooapis.com' 

REQUEST_TOKEN_URL = 'https://fireeagle.yahooapis.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://fireeagle.yahooapis.com/oauth/access_token'
AUTHORIZATION_URL = 'http://fireeagle.yahoo.net/oauth/authorize'
QUERY_API_URL = 'https://fireeagle.yahooapis.com/api/0.1/user'
UPDATE_API_URL = 'https://fireeagle.yahooapis.com/api/0.1/update'

# key and secret you got from Fire Eagle when registering an application
CONSUMER_KEY = 'MA50vzScwrQY'
CONSUMER_SECRET = 'hWGs0myHklpZ1ouBI0MmlweVCwZGdpva'

class FireEagleHandler(webapp.RequestHandler):
	def get(self):
		print 1
		print 1

# databases
class Place(db.Model):
  #__key__ is id
	name = db.StringProperty()
	placeID = db.IntegerProperty()
	emailName = db.StringProperty()
	
class CurrentPlace(db.Model):
	#__key__ is id
	thePlace = db.IntegerProperty()
	weekNum = db.IntegerProperty()
			
def getTodaysPlace():
	query = db.Query(CurrentPlace)
	query.filter('weekNum',0)
	todaysEvent = query[0]
	query = db.Query(Place)
	query.filter('placeID',todaysEvent.thePlace)
	return query[0]
	
class TestHandler(webapp.RequestHandler):
	def get(self):
		print 1
		print 1 

class UpdatePlacesHandler(webapp.RequestHandler):
	def get(self):
		newQuery = db.Query(Place)
		newQuery.filter('placeID',0)
		a = newQuery[0]
		a.emailName = "Online Only"
		a.put()
		newQuery1 = db.Query(Place)
		newQuery1.filter('placeID',1)
		b = newQuery1[0]
		b.emailName = "Mujo's"
		b.put()
		newQuery2 = db.Query(Place)
		newQuery2.filter('placeID',2)
		c = newQuery2[0]
		c.emailName = "Central Campus"
		c.put()

class TweetHandler(webapp.RequestHandler):
	def get(self):
		api = twitter.Api(username='coffeehousecode', password='bobdole')

		message = 'This week #coffeehousecoders is '
		todaysPlace = getTodaysPlace()
		message += todaysPlace.name
		# twitter doesn't like repeat messages, so we add/remove
		# a period at the end of our tweet to ensure it goes through
		# for a given week
		if datetime.datetime.now().isocalendar()[1] % 2:
			message += "."
		status = api.PostUpdate(message)
		
		print status		

class FollowHandler(webapp.RequestHandler):
	def get(self):
		th.follow_unfollowed()

class EmailHandler(webapp.RequestHandler):
	def get(self):
		subject = "CoffeeHouseCoders - Tonight - "
		todaysPlace = getTodaysPlace()
		subject += todaysPlace.emailName

		message = mail.EmailMessage(sender="CoffeeHouseCoder@gmail.com")
		message.to = "CoffeeHouseCoders <coffeehousecoders@googlegroups.com>"
		message.subject = subject
		message.body = """
		Hey Everyone,

		So if you are getting this e-mail it means that the cron jobs work and
		we can inform you of CoffeeHouseCoder's location automatically.  Come
		hang out this week and hack the night away, maybe even make this little
		automated script do more than just a few twitter/e-mail/Fire Eagle updates.
		
		You can also follow the twitter bot (http://twitter.com/coffeehousecode)
		to get more info or check out who else it talking about coffeehousecoders
		(http://twitter.com/search?q=coffeehousecoders)

		===============
		WHAT:
		 Informal hack group - http://coffeehousecoders.org/
		WHERE: 
		 """

		message.body += todaysPlace.name

		message.body +="""
		 irc.freenode.net:#coffeehousecoders
		WHEN:
		 Wednesdays (tonight!) 9-11PM EST
		===============

		-- 
		Meet, drink, hack - http://coffeehousecoders.org/
		Calling all geeks! - http://a2geeks.org/
		"""

		message.send()

class AdminHandler(webapp.RequestHandler):

	def get(self):
		template_values={}
		template_values['locations'] = Place.all().fetch(limit=10)
		template_values['week0'] = db.Query(CurrentPlace).filter('weekNum',0)[0].thePlace
		template_values['week1'] = db.Query(CurrentPlace).filter('weekNum',1)[0].thePlace
		template_values['week2'] = db.Query(CurrentPlace).filter('weekNum',2)[0].thePlace
		template_values['week3'] = db.Query(CurrentPlace).filter('weekNum',3)[0].thePlace
		path = os.path.join(os.path.dirname(__file__), 'adminForm.html')
		self.response.out.write(template.render(path,template_values))

class FutureHandler(webapp.RequestHandler):

	def post(self):
		place1 = db.Query(CurrentPlace)
		place2 = db.Query(CurrentPlace)
		place3 = db.Query(CurrentPlace)
		place4 = db.Query(CurrentPlace)
		place1.filter('weekNum',0)
		place2.filter('weekNum',1)
		place3.filter('weekNum',2)
		place4.filter('weekNum',3)
		a = place1[0]
		b = place2[0]
		c = place3[0]
		d = place4[0]
		a.thePlace = int(self.request.get("week1"))
		b.thePlace = int(self.request.get("week2"))
		c.thePlace = int(self.request.get("week3"))
		d.thePlace = int(self.request.get("week4"))
		a.put()
		b.put()
		c.put()
		d.put()

class NextWeekHandler(webapp.RequestHandler):
	def get(self):
		# shifts the place of CHC to where it will be next week
		week0 = db.Query(CurrentPlace).filter('weekNum',0)[0]
		week1 = db.Query(CurrentPlace).filter('weekNum',1)[0]
		week2 = db.Query(CurrentPlace).filter('weekNum',2)[0]
		week3 = db.Query(CurrentPlace).filter('weekNum',3)[0]
		temp = week0.thePlace
		week0.thePlace = week1.thePlace
		week1.thePlace = week2.thePlace
		week2.thePlace = week3.thePlace
		week3.thePlace = temp
		week0.put()
		week1.put()
		week2.put()
		week3.put()
		


def main():
  application = webapp.WSGIApplication([('/update/tweet', TweetHandler),
																				('/update/tweet/follows', FollowHandler),
																				('/update/email', EmailHandler),
																				('/update/admin', AdminHandler),
																				('/update/admin/future', FutureHandler),
																				('/update/nextweek', NextWeekHandler),
																				('/update/test', TestHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()