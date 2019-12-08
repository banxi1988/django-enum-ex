PROJECT_APPS = ('django_enum_ex', 'tests.testapp',)

INSTALLED_APPS = (
                   'django.contrib.contenttypes',
               ) + PROJECT_APPS

SECRET_KEY = 'this is a test app'
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
  }
}