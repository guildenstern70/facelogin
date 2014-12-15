import time

import webapp2
from webapp2_extras import sessions

import db
import main
import login


class BasePage(webapp2.RequestHandler):
    
    def __init__(self, request, response):
        """ constructor """
        
        main.log('Initializing base page.')      
        # Set self.request, self.response and self.app.
        self.initialize(request, response)
        
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        
        # Initalize user session
        self._initialize_login()
        
    def dispatch(self):
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        session = None
        if (self.session_store):
            session = self.session_store.get_session()
        return session
    
    def _initialize_login(self):
        main.log('Initializing login from session.')       
        try:
            login_object = self.session['login_obj']
            self.logged = login_object
            main.log('Login object found in session')
        except KeyError:
            main.log('Login object NOT FOUND')
            self.logged = login.Logged()
        if self.logged.is_logged:
            main.log('Logged in with ' + self.logged.nick)
        else:
            main.log('User not logged in')
                 
    def _set_template_vals(self, template_vals):                                  
        init_template_values = {
            'login_url': '/login',
            'logout_url': '/logout',
            'loginobj': self.logged
        }
        if (template_vals != None):
            self.template_values = dict(init_template_values.items() + template_vals.items())
        else:
            self.template_values = init_template_values
         
    def render(self, template_vals, template_page): 
        
        if not self.logged.is_logged:
            template_page = 'index.html'
            template_vals = None
            
        self._set_template_vals(template_vals)
        template = main.JINJA_ENVIRONMENT.get_template(template_page)
        self.response.write(template.render(self.template_values))
        

class Login(webapp2.RequestHandler):
    
    def get(self):
        email = self.request.get('email')
        name = self.request.get('name')
        nick = self.request.get('nick')
        main.log('User '+ nick +' wants to login: ' + email)
        self.logged.login(name, nick, email)
        self.redirect('/')
    
class Logout(BasePage):
    
    def get(self):
        self.session.pop('login_obj', None)
        self.redirect('/')
    
class DeleteUser(webapp2.RequestHandler):
    
    def get(self):     
        who = self.request.get('user')
        main.log('Asked to delete user: ' + who)
        db.Queries.delete_user(who)
        time.sleep(1)
        self.redirect('/users')

class Account(BasePage):
    
    def get(self):
        user_email = self.logged.email
        template_values = { 
            'user' : db.Queries.get_db_user(user_email)
        }
        self.render(template_values, 'account.html')
    
class Users(BasePage):
    
    def get(self):
        template_values = { 
            'users' : db.Queries.get_all_users(),
            'currentuser' : self.logged.email
        }
        self.render(template_values, 'users.html')
        

class MainPage(BasePage):
    
    def post(self):           
        email = self.request.get('email')
        name = self.request.get('name')
        nick = self.request.get('nick')
        main.log('User '+ nick +' wants to login: ' + email)
        self.logged.login(name, nick, email)
        self.render(None, 'index.html')
        
    def get(self):                
        self.render(None, None)  
        
