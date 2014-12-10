import webapp2

import google.appengine.api.users as users

import main
import time
import db

class BasePage(webapp2.RequestHandler):
      
    def __set_template_vals(self, template_vals, google_user):  
        
        isin = False
        nick = ""
            
        if google_user:
            main.log('Logged in with ' + google_user.nickname())
            isin = True
            nick = google_user.nickname()
        else:
            main.log('User not logged')
        
        init_template_values = {
            'login_url': users.create_login_url('/'),
            'logout_url': users.create_logout_url('/'),
            'is_logged_in': isin,
            'user_nick': nick
        }
        
        if (template_vals != None):
            self.template_values = dict(init_template_values.items() + template_vals.items())
        else:
            self.template_values = init_template_values
         
    def render_with_user(self, google_user, template_vals, template_page):       
        self.__set_template_vals(template_vals, google_user)
        template = main.JINJA_ENVIRONMENT.get_template(template_page)
        self.response.write(template.render(self.template_values))
        
    def render(self, template_vals, template_page):
        self.render_with_user(users.get_current_user(), template_vals, template_page)

class DeleteUser(webapp2.RequestHandler):
    
    def get(self):     
        who = self.request.get('user')
        main.log('Asked to delete user: ' + who)
        db.Queries.delete_user(who)
        time.sleep(1)
        self.redirect('/users')
    
class Users(BasePage):
    
    def get(self):
        template_values = { 'users' : db.Queries.get_all_users() }
        self.render(template_values, 'users.html')
        

class MainPage(BasePage):
    
    def get(self):
        user = users.get_current_user()
        if (user != None):
            db.Queries.check_or_register_user(user)
        self.render_with_user(user, None, 'index.html')
        
