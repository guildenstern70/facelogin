from db import Queries

class WebUser(object):
    
    def __init__(self):
        self.__logged = False
        self.__nickname = ''
        self.__name = ''
        self.__email = ''
    
    def __is_logged(self):
        return self.__logged
    
    def __set_logged(self, value):
        self.__logged = value
        
    def __update_or_create_on_db(self):
        Queries.update_or_register_user(self)
        
    def login(self, name, nickname, email):
        self.__email = email
        self.__name = name
        self.__nickname = nickname
        self.__logged = True
        self.__update_or_create_on_db()
        
    def login_from_google(self, google_user):
        self.__email = google_user.email()
        self.__name = google_user.nickname()
        self.__nickname = google_user.nickname()
        self.__logged = True
        
    def logout(self):
        self.__email = ''
        self.__name = ''
        self.__nickname = ''
        self.__logged = False
         
    @property
    def email(self):
        return self.__email
    
    @property
    def name(self):
        return self.__name
    
    @property
    def nick(self):
        return self.__nickname
    
    def __repr__(self):
        return 'WebUser '+ self.__nickname + ' ('+ self.__email + ')'
    
    @classmethod   
    def fromEmail(self, email):
        dbuser = Queries.get_db_user(email)
        webuser = WebUser()
        if dbuser != None:
            webuser.login(dbuser.name, dbuser.nickname, email)
        return webuser
      
    def get_db_user(self):
        return Queries.get_db_user(self.__email)
           
    is_logged = property(__is_logged, __set_logged,
                     doc="""Gets or sets if the user is logged.""")
    
    
    