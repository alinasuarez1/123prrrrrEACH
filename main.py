import os
import webapp2
import socialdata

from google.appengine.api import images

from google.appengine.ext.webapp import template
from google.appengine.api import users     #Really useful to get information from users. Allos to generate URLS
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


def render_template(handler, file_name, template_values):           #puts the template sent on the main page
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None

def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
        values['profileedit_url'] = '/profileedit'
        values['upload_url'] = blobstore.create_upload_url('/profile-save')
        values['home_url'] = '/home'
    else:
        values['login_url'] = users.create_login_url('/')
    return values


class MainHandler(webapp2.RequestHandler):          #Request handlers accepts a request and gives back a response
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['firstname'] = profile.firstname
        render_template(self, 'homepage.html', values)    #calling render_template function
        self.redirect('/home')
        

class HomeHandler(webapp2.RequestHandler):  # DONT TOUCH
    def get(self):
        values = get_template_parameters()
        profile = socialdata.get_user_profile(get_user_email())
        if profile:
            values['firstname'] = profile.firstname
            values['nickname'] = profile.nickname
        render_template(self, 'homepage.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'profileedit.html', values)

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        profile = socialdata.get_user_profile(get_user_email())
        if profile:
            values['firstname'] = profile.firstname
            values['nickname'] = profile.nickname
        render_template(self, 'upload.html', values)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile = socialdata.get_user_profile(get_user_email())
        values = get_template_parameters()
        render_template(self, 'profile.html', values)
        values['firstname'] = profile.firstname


class FeedHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdata.get_recent_profiles()
        values = get_template_parameters()
        values['profiles'] = profiles
        render_template(self, 'feed.html', values) 

class ProfileViewHandler(webapp2.RequestHandler):
    def get(self, firstname):
        profile = socialdata.get_profile_by_name(firstname)
        values = get_template_parameters()
        values['firstname'] = "unknown"
        values['lastname'] = "unknown"
        values['age'] = "unknown"
        values['description'] = " "
        values['nationality'] = "unknown"
        values['location'] = "unknown"
        values['language'] = "unknown"
        if profile: 
            values['firstname'] = profile.firstname
            values['lastname'] = profile.lastname
            values['age'] = profile.age
            values['description'] = profile.description
            values['nationality'] = profile.nationality
            values['location'] = profile.location
            values['language'] = profile.language
            values['userid'] = profile.key.urlsafe()
        render_template(self, 'profileview.html', values)


class ProfileSaveHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            upload_files = self.get_uploads()
            blob_info = upload_files[0]
            content_type = blob_info.content_type
            profilepic = blob_info.key()
            print "Got a blob key. "
            print profilepic

            if content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                error_text += 'Type should be image.\n'
            firstname = self.request.get('firstname')
            lastname = self.request.get('lastname')
            age = self.request.get('age')
            description = self.request.get('description')
            nationality = self.request.get('nationality')
            location = self.request.get('location')
            nickname = self.request.get('nickname')
            language = self.request.get('language')

            # if len(name) < 2:
            #     error_text += 'name should be at least two characters. \n'
            # if len(name) > 20:
            #     error_text += 'name should be no more than 20 characters. \n'
            # if len(name.split()) > 1:
            #     error_text += 'name should not have whitespace. \n'
            # if len(description) > 4000:
            #     error_text += 'Description should be less than 4000 characters. \n'

            # for word in description.split():
            #     if len(word) > 50:
            #         error_text += 'Description contains words that are too long.\n'
            #         break
            values = get_template_parameters()
            values['firstname'] = firstname
            values['lastname'] = lastname
            values['age'] = age
            values['description'] = description
            values['nationality'] = nationality
            values['location'] = location
            values['language'] = language
            varname = firstname[:9]
            values['nickname'] = varname
            #values['profilepic'] = blob_info.key()
            
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdata.save_profile(email, firstname, lastname, age, description, nationality, location, language, varname, profilepic) 
                values['successmsg'] = 'Everything worked out fine'    
            render_template(self, 'profileedit.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['firstname'] = profile.firstname
                values['lastname'] = profile.lastname
                values['nickname'] = profile.nickname
                values['age'] = profile.age
                values['description'] = profile.description
                values['nationality'] = profile.nationality
                values['location'] = profile.location
                values['language'] = profile.language
                #values['profilepic'] = profile.profilepic
            render_template(self, 'profileedit.html', values)


class ImageHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user_id = self.request.get('user')
        print "Received user ID: " + user_id
        user_profile = ndb.Key(urlsafe=user_id).get()
        self.send_blob(user_profile.profilepic)




class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe='aghkZXZ-Tm9uZXIYCxILVXNlclByb2ZpbGUYgICAgICA6AkM')
        key.delete()
        self.response.out.write('deleted')
        

app = webapp2.WSGIApplication([         #Anything that isn't specified goes to the main page
    ("/home", HomeHandler),
    ('/profileedit', ProfileEditHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profileview/(.*)', ProfileViewHandler),
    ('/profilepic', ImageHandler),
    ('/upload', UploadHandler),
    ('/profile', ProfileHandler),
    ('/feed', FeedHandler),
    ('/deletor', DeleteHandler),
    ('.*', MainHandler),
])