from django.contrib.auth.models import User
from django.db.utils import IntegrityError

email = 'admin@example.com'
password = 'openclassadmin'

try:
    User.objects.get(username='admin')
    print ("User 'admin' already exist")
except User.DoesNotExist:
    User.objects.create_superuser('admin', email, password)
    print ("User 'admin created with default password'")
