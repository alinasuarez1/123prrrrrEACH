from google.appengine.ext import ndb



class Video(ndb.Model):
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    language = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty()


class UserProfile(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    videos = ndb.KeyProperty(Video, repeated=True)
    age = ndb.StringProperty()
    nickname = ndb.StringProperty()
    email = ndb.StringProperty()
    description = ndb.TextProperty()
    location = ndb.StringProperty()
    language = ndb.StringProperty()
    nationality = ndb.StringProperty()
    profilepic = ndb.BlobKeyProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)  #Sets property to the time it is updated
    # "Age"
    # "loaction"
    # "language"
    # "speaker = False/True"
