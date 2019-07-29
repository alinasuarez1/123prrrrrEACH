from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    age = ndb.StringProperty()
    email = ndb.StringProperty()
    description = ndb.TextProperty()
    location = ndb.StringProperty()
    language = ndb.StringProperty()
    nationality = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)  #Sets property to the time it is updated
    # "Age"
    # "loaction"
    # "language"
    # "speaker = False/True"