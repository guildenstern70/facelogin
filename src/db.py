import main

from google.appengine.ext import ndb
 
class DbUser(ndb.Model):
    """ DB Schema: DbFableUser """
    
    user = ndb.UserProperty(required=True)
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    nickname = ndb.StringProperty()
    added = ndb.DateTimeProperty(auto_now_add=True)
    
    @staticmethod
    def get_from_user(google_user):
        """ Get the user record from Google user """
        user_key = ndb.Key('DbUser', google_user.email())
        return user_key.get()
    
    @staticmethod
    def create_user(google_user):
        """ Create a user record """
        usermail = google_user.email()
        user_key = ndb.Key(DbUser, usermail);
        userdb = DbUser(key = user_key, user = google_user, email = usermail, 
                        name = "??", 
                        nickname = google_user.nickname())
        main.log('Adding user ' + usermail + ' to DB...')
        userdb.put()
        main.log('User added. ')
    
    def __repr__(self):
        return "DbUser [user="+self.email+"]"
    
class Queries():
      
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
    def check_or_register_user(google_user):
        user_record = DbUser.get_from_user(google_user)
        if (user_record != None):
            main.log('User was on DB: ')
        else:
            main.log('User not found on DB: adding')
            DbUser.create_user(google_user)


        
    