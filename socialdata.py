from socialmodels import UserProfile

def save_profile(email, firstname, lastname, age, description, nationality, location, language, nickname):
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
    else:
        p = UserProfile(email = email, firstname= firstname, lastname=lastname, description=description, nationality=nationality, location=location, language=language, nickname=nickname )
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
    return q.fetch(10)