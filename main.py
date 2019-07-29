import os
import webapp2
import socialdata

from google.appengine.ext.webapp import template
from google.appengine.api import users     #Really useful to get information from users. Allos to generate URLS

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
        values['upload_url'] = '/upload'
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
                values['name'] = profile.name
        render_template(self, 'homepage.html', values)    #calling render_template function
        self.redirect('/home')
        

class HomeHandler(webapp2.RequestHandler):  # DONT TOUCH
    def get(self):
        values = get_template_parameters()
        render_template(self, 'homepage.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'profileedit.html', values)

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'upload.html', values)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'profile.html', values)

class FeedHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'feed.html', values)






app = webapp2.WSGIApplication([         #Anything that isn't specified goes to the main page
    ("/home", HomeHandler),
    ('/profileedit', ProfileEditHandler),
    ('/upload', UploadHandler),
    ('/profile', ProfileHandler),
    ('/feed', FeedHandler),
    ('.*', MainHandler),
])