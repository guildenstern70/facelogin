""" 
 
 FaceLogin.com 
 A LittleLite Web Application
 (c) 2014
 
 main.py
 
"""


import logging
import jinja2
import webapp2
import os

import google.appengine.api.users as users

logging.getLogger().setLevel(logging.DEBUG)  

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        isin = False
        nick = ""
        
        if user:
            logging.info('Logged in with ' + user.nickname())
            isin = True
            nick = user.nickname()
        else:
            logging.info('User not logged')

        template_values = {
            'login_url': users.create_login_url('/'),
            'logout_url': users.create_logout_url('/'),
            'is_logged_in': isin,
            'user_nick': nick
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


APPLICATION = webapp2.WSGIApplication(
                            [ ('/', MainPage)
                             ], debug = True)
                             

