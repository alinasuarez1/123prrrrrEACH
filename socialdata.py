from socialmodels import UserProfile
from socialmodels import Video

def save_profile(email, firstname, lastname, age, description, nationality, location, language, nickname, profilepic):
    p = get_user_profile(email)
    if p:
        p.firstname = firstname
        p.lastname = lastname
        p.age = age
        p.description = description
        p.nationality = nationality
        p.location = location
        p.language = language
        p.nickname = nickname
        p.profilepic = profilepic
    else:
        p = UserProfile(email = email, firstname= firstname, lastname=lastname, description=description, nationality=nationality, location=location, language=language, nickname=nickname ,profilepic=profilepic)
    p.put()       #saves it in the database

def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_profile_by_name(firstname):
    q = UserProfile.query(UserProfile.firstname == firstname)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_recent_profiles():      #Can use on the feed, to return profiles/videos of recent users
    q = UserProfile.query().order(-UserProfile.last_update)
    return q.fetch(50)

def get_videos(var):
    v = Video.query().order(-Video.last_update)
    return v.fetch(var)

def upload_video(email ,url, description, language, title):
    profile = get_user_profile(email)
    
    v = Video(email = email, title= title, description=description, language=language, url=url)
    var = v.put()
    profile.videos.append(var)
    profile.put()

def follow_user(emailfollower, emailfollowing):
    if emailfollower != emailfollowing:
        ufollower = get_user_profile(emailfollower)     #grabs profile of whoever followed
        ufollowing = get_user_profile(emailfollowing)   #grabs profile of whoever is being followed
        print("follow_user before if")
        print(ufollower)
        print (ufollowing)
        if ufollower and ufollowing:
            print("profiles exist on followuser")
            if not(ufollowing.key.urlsafe()in ufollower.following):
                print("it is still going, somehow...")
                ufollower.following.append(ufollowing.key.urlsafe())
                ufollowing.followers.append(ufollower.key.urlsafe())
        ufollower.put()
        ufollowing.put()
    else:
        print("you can't follow yourself dummy")