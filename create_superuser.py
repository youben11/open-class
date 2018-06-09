from django.contrib.auth.models import User
from django.db.utils import IntegrityError

email = 'admin@example.com'
password = 'openclassadmin'

try:
    User.objects.create_superuser('admin', email, password)
except:
    try:
        User.objects.get(username='admin')
        print ("User 'admin' already exist")
    except:
        pass
