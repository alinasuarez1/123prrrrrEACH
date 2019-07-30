from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    age = ndb.StringProperty()
    nickname = ndb.StringProperty()
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

class VideoStructure(ndb.Model):
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    language = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty()