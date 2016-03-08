import os
from django.conf import settings
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ADMINS = [('Webmaster','dmcgweb101@gmail.com'), ('Manager', 'errors@photozero.co.uk')]

DATABASES = settings.DATABASES

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# STATICFILES and MEDIAFILES STORAGE

AWS_ACCESS_KEY_ID = 'AKIAIB34RHLINXD54E4Q'
AWS_SECRET_ACCESS_KEY = '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'

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'photozero.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'photozero.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'photozerobasic'
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

import datetime

date_two_months_later = datetime.date.today() + datetime.timedelta(2 * 365 / 12) 
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=86400',
}
