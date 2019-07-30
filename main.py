import os
import webapp2
import socialdata
from google.appengine.ext import ndb


from google.appengine.ext.webapp import template
# Really useful to get information from users. Allos to generate URLS
from google.appengine.api import users


# puts the template sent on the main page
def render_template(handler, file_name, template_values):
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


# Request handlers accepts a request and gives back a response
class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
<<<<<<< HEAD
                values['name'] = profile.name
        # calling render_template function
        render_template(self, 'homepage.html', values)
=======
                values['firstname'] = profile.firstname
        render_template(self, 'homepage.html', values)    #calling render_template function
>>>>>>> 0e46f10b637c3649447f5caf9534c689f0d90f2e
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
    def get(self):
        profile = socialdata.get_profile_by_name(profile.firstname)
        values = get_template_parameters()
        render_template(self, 'feed.html', values)


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            title = self.request.get('title')
            url = self.request.get('videourl')
            description = self.request.get('vdescription')
            language = self.request.get('language')

            if len(title) < 2:
                error_text += 'name should be at least two characters. \n'
            if len(title) > 20:
                error_text += 'name should be no more than 20 characters. \n'
            if len(description) > 4000:
                error_text += 'Description should be less than 4000 characters. \n'

            for word in description.split():
                if len(word) > 50:
                    error_text += 'Description contains words that are too long.\n'
                    break
            values = get_template_parameters()
            values['title'] = title
            values['url'] = url
            values['description'] = description
            values['language'] = language
            render_template(self, 'upload.html', values)

    def post(self):
        title = self.request.get('title')
        url = self.request.get('videourl')
        description = self.request.get('vdescription')
        language = self.request.get('language')
        email = get_user_email()
        socialdata.upload_video(email, url, description, language, title)
        self.redirect('/')

    # def get(self):
    #     email = get_user_email()
    #     if not email:
    #         self.redirect('/')
    #     else:
    #         values = get_template_parameters()
    #         profile = socialdata.get_user_profile(get_user_email())
    #         if profile:
    #             values['name'] = profile.name
    #             values['nickname'] = profile.nickname
    #         render_template(self, 'upload.html', values)

        values['firstname'] = 'Unknown'
        values['description'] = 'Profile does not exist'
        if profile: 
            values['firstname'] = profile.firstname
            values['description'] = profile.description
        render_template(self, 'profileview.html', values)
        
class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
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

            if error_text:
                values['errormsg'] = error_text
            else:

                socialdata.save_profile(email, firstname, lastname, age, description, nationality, location, language, varname) 
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
            render_template(self, 'profileedit.html', values)

app = webapp2.WSGIApplication([  # Anything that isn't specified goes to the main page
    ("/home", HomeHandler),
    ('/profileedit', ProfileEditHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profileview', ProfileViewHandler),
    ('/upload', UploadHandler),
    ('/profile', ProfileHandler),
    ('/feed', FeedHandler),
    ('.*', MainHandler),
])
