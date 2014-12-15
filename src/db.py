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
        main.log('User updated or added. ')
    
    def __repr__(self):
        return "DbUser [user="+self.email+"]"
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
    
class Queries():
    
    @staticmethod
    def get_db_user(user_email):
        
        if user_email == '':
            return None
        
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
    def update_or_register_user(logged_in_user):
        user_record = DbUser.get_from_login(logged_in_user)
        if (user_record != None):
            main.log('User found on DB... ')
            if (user_record.name != logged_in_user.name):
                main.log('Updating name from ' + user_record.name + ' to ' + logged_in_user.name)
                user_record.name = logged_in_user.name
                user_record.put()
            if (user_record.nickname != logged_in_user.nick):
                main.log('Updating nick from ' + user_record.nickname + ' to ' + logged_in_user.nick)
                user_record.nickname = logged_in_user.nick
                user_record.put()
        else:
            main.log('User not found on DB: adding')
            DbUser.create_from_login(logged_in_user)


        
    