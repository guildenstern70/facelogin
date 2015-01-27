""" 
 
 FaceLogin.com 
 A LittleLite Web Application
 (c) 2014
 
 main.py
 
"""


import logging
import os

import jinja2
import webapp2

import pages

logging.getLogger().setLevel(logging.DEBUG)  

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'bludream',
}

APPLICATION = webapp2.WSGIApplication(
                            [ ('/', pages.MainPage),
                              ('/users', pages.Users),
                              ('/deleteuser', pages.DeleteUser),
                              ('/account', pages.Account),
                              ('/login', pages.Login),
                              ('/addfable', pages.AddFable),
                              ('/logout', pages.Logout)
                             ], debug = True, config = config)

def log(message):
    logging.debug('[*** '+ message + '***]')

                             

