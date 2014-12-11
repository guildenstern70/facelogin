import time

from google.appengine.ext.webapp.util import login_required
import webapp2
from webapp2_extras import sessions

import db
import main
import login


class BasePage(webapp2.RequestHandler):
    
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    def __initialize_login(self):
        main.log('Initializing login from session.')       
        try:
            login_object = self.session['login_obj']
            self.logged = login_object
            main.log('Login object found in session')
        except KeyError:
            main.log('Login object NOT FOUND')
            self.logged = login.Logged()
                 
    def __set_template_vals(self, template_vals):         
        
        self.__initialize_login()
                    
        if self.logged.is_logged:
            main.log('Logged in with ' + self.logged.nick)
        else:
            main.log('User not logged in')
        
        init_template_values = {
            'login_url': '/login',
            'logout_url': '/logout',
            'is_logged_in': self.logged.is_logged,
            'user_nick': self.logged.nick
        }
        
        if (template_vals != None):
            self.template_values = dict(init_template_values.items() + template_vals.items())
        else:
            self.template_values = init_template_values
         
    def render(self, template_vals, template_page):  
        self.__set_template_vals(template_vals)
        template = main.JINJA_ENVIRONMENT.get_template(template_page)
        self.response.write(template.render(self.template_values))
        

class Login(webapp2.RequestHandler):
    
    def get(self):
        email = self.request.get('email')
        main.log('User wants to login: ' + email)
        pass
    
class Logout(webapp2.RequestHandler):
    
    def get(self):
        self.redirect('/')
    
class DeleteUser(webapp2.RequestHandler):
    
    @login_required
    def get(self):     
        who = self.request.get('user')
        main.log('Asked to delete user: ' + who)
        db.Queries.delete_user(who)
        time.sleep(1)
        self.redirect('/users')
    
class Users(BasePage):
    
    def get(self):
        template_values = { 
            'users' : db.Queries.get_all_users(),
            'currentuser' : self.logged.email
        }
        self.render(template_values, 'users.html')
        

class MainPage(BasePage):
    
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        nick = self.request.get('nick')
        main.log('Requesting LOGIN for ' + email)
        self.render(None, 'index.html')
        
    def get(self):                
        self.render(None, 'index.html')
        
