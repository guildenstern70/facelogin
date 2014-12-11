import main

from google.appengine.ext import ndb
 
class DbUser(ndb.Model):
    """ DB Schema: DbUser """
    
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    nickname = ndb.StringProperty()
    added = ndb.DateTimeProperty(auto_now_add=True)
    
    @staticmethod
    def get_from_login(logged_user):
        """ Get the user record from Google user """
        user_key = ndb.Key('DbUser', logged_user.email)
        return user_key.get()
    
    @staticmethod
    def get_from_email(email):
        """ Get the user record from email """
        user_key = ndb.Key('DbUser', email)
        return user_key.get()
    
    @staticmethod
    def create_from_login(logged_user):
        """ Create a user record """
        usermail = logged_user.email
        nickname = logged_user.nick
        name = logged_user.name
        DbUser.create(usermail, name, nickname)
        
    @staticmethod
    def create(usermail, username, nick):
        user_key = ndb.Key(DbUser, usermail);
        userdb = DbUser(key = user_key, email = usermail, name = username, 
                        nickname = nick)
        main.log('Adding user ' + usermail + ' to DB...')
        userdb.put()
        main.log('User added. ')
    
    def __repr__(self):
        return "DbUser [user="+self.email+"]"
    
class Queries():
    
    @staticmethod
    def get_db_user(user_email):
        user_key = ndb.Key('DbUser', user_email)
        return user_key.get()
      
    @staticmethod     
    def get_all_users(): 
        return DbUser.query()
    
    @staticmethod     
    def delete_user(user_email): 
        user_key = ndb.Key('DbUser', user_email)
        if (user_key != None):
            user_key.delete()
            main.log('Deleted user ' + user_email)
        else:
            main.log('Cannot delete: unknown user ' + user_email)
            
    @staticmethod    
    def check_or_register_user(logged_in_user):
        user_record = DbUser.get_from_login(logged_in_user)
        if (user_record != None):
            main.log('User found on DB... ')
        else:
            main.log('User not found on DB: adding')
            DbUser.create_from_login(logged_in_user)


        
    