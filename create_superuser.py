from django.contrib.auth.models import User
from django.db.utils import IntegrityError

email = 'admin@example.com'
password = 'openclassadmin'

try:
    User.objects.create_superuser('admin', email, password)
except IntegrityError:
    admin = User.objects.get(username='admin')
    admin.set_password(password)
    admin.save()
