#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import urllib
import urllib2
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import twitter


class BaseRequestHandler(webapp.RequestHandler):
    """Base request handler extends webapp.Request handler.

       It defines the generate method, which renders a Django template
       in response to a web request.
    """

    def generate(self, template_name, template_values={}):
        """Renders HTML template with the specified values."""

        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'templates', template_name)
        self.response.out.write(template.render(path, template_values, debug=True))


class MainHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>Who are we?</h2>
                <p>
                If you're new to coding or a seasoned hacker, CoffeeHouseCoders is for you. We meet once a week in local coffee shops to work on pet projects, talk about technology, and meet our fellow hackers.
                </p>

                <p>Sound like your kind of thing?</p>

                <div class="flickr">
                    <object class="flickr" width="300" height="200">

                        <param name="flashvars" value="&offsite=true&amp;lang=en-us&page_show_url=%2Fsearch%2Fshow%2F%3Fq%3Dcoffeehousecoders&page_show_back_url=%2Fsearch%2F%3Fq%3Dcoffeehousecoders&method=flickr.photos.search&api_params_str=&api_text=coffeehousecoders&api_tag_mode=bool&api_sort=relevance&jump_to=&start_index=0">
                        </param>
                        <param name="movie" value="http://www.flickr.com/apps/slideshow/show.swf?v=67348">
                        </param>
                        <param name="allowFullScreen" value="true">
                        </param>
                        <embed type="application/x-shockwave-flash" src="http://www.flickr.com/apps/slideshow/show.swf?v=67348" allowFullScreen="true" flashvars="&offsite=true&amp;lang=en-us&page_show_url=%2Fsearch%2Fshow%2F%3Fq%3Dcoffeehousecoders&page_show_back_url=%2Fsearch%2F%3Fq%3Dcoffeehousecoders&method=flickr.photos.search&api_params_str=&api_text=coffeehousecoders&api_tag_mode=bool&api_sort=relevance&jump_to=&start_index=0" width="400" height="300">
                        </embed>
                    </object>
                </div>

                <h2>Join up!</h2>

                <p>
                    Find a <a href="/locations/">meetup location near you</a>.
                    You can also <a href="/irc/">chat with us on IRC</a>.
                </p>
                """})


class AboutHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>Breif History</h2>
                <p>
                CoffeeHouseCoders was started in 2008 by mjpizz and steiza to hack on side projects outside of work. It quickly grew to several hackers in the Ann Arbor area and has evolved into a super-informal weekly hacker meetup.
                </p>
                <p>
                There's no "meeting format", people just show up and do what they want: coding, whiteboarding and idea with friends, arguing about technology, or finding startup co-founders.
                </p>
                <p>
                We love CoffeeHouseCoders so much, we put together this site to make it even easier to organize a meetup. Find a <a href="/locations/">location near you</a> or <a href="/advice/">start your own</a>.
                </p>
                """})


class AdviceHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>Starting a group</h2>
                <p>
                Rock on! It's pretty easy to organize a meetup, just pick a time, place, and show up. <a href="mailto:startup@coffeehousecoders.org">Send us an e-mail</a> and we can add you to the <a href="/locations/">list of locations</a>. Below is some advice we wished someone told us when we were getting started:
                </p>

                <h2>Picking a meeting time</h2>
                <p>
                You probably want to once a week or once a month. Meeting weekly is easier to explain ('we meet every Wednesday' instead of 'second Wednesday of every month') and it's easier for people to work into their schedules, even if they can't make it to every meeting. If you decide to meet once a month, consider doing something like <a href='http://superhappydevhouse.org/'>SuperHappyDevHouse</a>. We meet Wednesdays, 9-11PM EST (plus or minus a few hours), and that's definitely when the <a href="/irc/">IRC channel</a> is most active. Pick a time you know at least you and one other person can make it.
                </p>

                <h2>Pick a location</h2>
                <p>
                Wherever you meet, it must have good Internet! Hell hath no fury like offline geeks. For meeting weekly, make sure there's also good coffee/snacks; when meeting monthly some place you can bring in pizza and beer is nice. Coffee shops, bars, university buildings, or local hacker spaces are all good places to meet. You might want to check out a few venues initially, but pick one fairly quickly, so people don't get confused.
                </p>

                <h2>Meet!</h2>
                <p>
                This is the fun part! Tell a bunch of people about the event, bring something distinctive (like <a href="http://www.flickr.com/photos/14799217@N08/3255426613/">a whiteboard</a> or <a href="http://lyfe.net/i/2803">laptop stickers</a>). Show up a little early and hack away!
                </p>
                """})


class IRCHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>Join us on IRC</h2>
                <p>
                    You can chat with us using any IRC client at
                    <span class="bright">
                        irc.freenode.net : #coffeehousecoders
                    </span>
                    or you can choose a username below and start chatting!
                </p>

                <iframe class="mibbit" width="100%" height="100%" src="http://widget.mibbit.com/?settings=e84f0fb60dd0c41b61a31c0b6dd8b0bf&server=irc.freenode.net&channel=%23coffeehousecoders&noServerNotices=true&noServerMotd=true&autoConnect=true">
                </iframe>
                """})


class LocationHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>Locations</h2>
                <p>Don't see your location below? <a href="/advice/">start your own</a>!</p>
                <div class="locations">
                    <ul>
                        <li>
                            <a href="/locations/ann_arbor.html">Ann Arbor, MI</a>
                        </li>
                        <li>
                            <a href="/locations/detroit.html">Detroit, MI</a>
                        </li>
                    </ul>
                </div>
                """})


class AnnArborHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <h2>When do we meet?</h2>
                <p>
                Every Wednesdays, from 9-11PM EST. We alternate between Espresso Royale Cafe on State St. and Mujo's in the Duderstadt Center on North Campus. Want to know where we're meeting this week? Check our niffty FireEagle applet:
                </p>

                <p>
                <div class="fireeagle_badge_main_container"><script type="text/javascript"src="http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=OpoSSWfV34F0BBl2kWn.ogVfnZrgxAVkQJiKaH_JdSatrueka6_Ut6Qnl0cZ"></script><div class="fireeagle_badge_map_container" id="fireeagle_map"></div><div id="fireeagle_badge" class="fireeagle_badge_data_container"><br /></div><script type="text/javascript" src="http://www.txtst.com/fireeagle_badge/fireeagle_badge.php?k=1h4mqnx69yfw208g&timezone=Eastern+Standard+Time&zoom=4"></script></div>
                </p>

                <h2>Projects</h2>
                <p>Want your project linked here? Come bug us!</p>
                """})

class DetroitHandler(BaseRequestHandler):

    def get(self):
        self.generate('base_page.html', {'content': """
                <p>We meet every Wednesday, from 7-10 EST, at:</p>
<pre>Caribou Coffee
1413 W 14 Mile Rd
Madison Heights, MI 48071</pre>

                <p>The last Wed of the month is a special longer edition that starts at 7pm.</p>
                <iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/maps?f=q&amp;source=embed&amp;hl=en&amp;geocode=&amp;q=caribou+coffee&amp;sll=42.577608,-83.145218&amp;sspn=0.144102,0.350189&amp;ie=UTF8&amp;radius=8.92&amp;rq=1&amp;cid=17926306267005349755&amp;ll=42.544038,-83.119726&amp;spn=0.037627,0.087547&amp;iwloc=A&amp;output=embed"></iframe><br /><small><a href="http://maps.google.com/maps?f=q&amp;source=embed&amp;hl=en&amp;geocode=&amp;q=caribou+coffee&amp;sll=42.577608,-83.145218&amp;sspn=0.144102,0.350189&amp;ie=UTF8&amp;radius=8.92&amp;rq=1&amp;cid=17926306267005349755&amp;ll=42.544038,-83.119726&amp;spn=0.037627,0.087547&amp;iwloc=A" style="text-align:left">View Larger Map</a></small>
                """})


def main():
    application = webapp.WSGIApplication(
            [
                ('/', MainHandler),
                ('/about/', AboutHandler),
                ('/advice/', AdviceHandler),
                ('/irc/', IRCHandler),
                ('/locations/', LocationHandler),
                ('/locations/ann_arbor.html', AnnArborHandler),
                ('/locations/detroit.html', DetroitHandler),
            ],
            debug=True)

    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
