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
        self.generate('index.html')


class AboutHandler(BaseRequestHandler):

    def get(self):
        self.generate('about.html')


class AdviceHandler(BaseRequestHandler):

    def get(self):
        self.generate('advice.html')


class IRCHandler(BaseRequestHandler):

    def get(self):
        self.generate('irc.html')


class LocationsHandler(BaseRequestHandler):

    def get(self):
        self.generate('locations.html')


class AnnArborHandler(BaseRequestHandler):

    def get(self):
        self.generate('locations/annarbor.html')

class DetroitHandler(BaseRequestHandler):

    def get(self):
        self.generate('locations/detroit.html')

class DownriverHandler(BaseRequestHandler):

    def get(self):
        self.generate('locations/downriver.html')

class LansingHandler(BaseRequestHandler):

    def get(self):
        self.generate('locations/lansing.html')


def main():
    application = webapp.WSGIApplication(
            [
                ('/', MainHandler),
                ('/about/', AboutHandler),
                ('/advice/', AdviceHandler),
                ('/irc/', IRCHandler),
                ('/locations/', LocationsHandler),
                ('/locations/ann_arbor.html', AnnArborHandler),
                ('/locations/detroit.html', DetroitHandler),
                ('/locations/downriver.html', DownriverHandler),
                ('/locations/lansing.html', LansingHandler),
            ],
            debug=True)

    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
