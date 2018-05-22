import os

def upload_to_profile_photo(instance, filename):
    root = 'profile/photos/'
    extension = os.path.splitext(filename)[-1]
    filename = instance.user.username
    return root + filename + extension

def upload_to_workshop_cover(instance, filename):
    root = 'workshop/covers/'
    extension = os.path.splitext(filename)[-1]
    filename = instance.title + '_' + str(int(instance.start_date.timestamp()))
    return root + filename + extension
