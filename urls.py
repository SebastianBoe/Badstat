from django.conf.urls.defaults import *

ROOT_PATTERN = r'^$'

urlpatterns = patterns('app.views',
    (r'[?]q=', 'search'),
    (ROOT_PATTERN, 'search'),
    (r'^klubber/$', 'clubs'),
    (r'^turneringer/$', 'tournaments'),
)
