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
        render_template(self, 'loginpage.html', values)     #calling render_template function


app = webapp2.WSGIApplication([         #Anything that isn't specified goes to the main page
    ('.*', MainHandler),
])