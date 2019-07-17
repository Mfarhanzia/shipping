from django.urls import path
from django.conf.urls import url
from .views import specialuser_signup, activate, admincheck

urlpatterns = [
    path('register/', specialuser_signup ,name='register'),

    url(r'^admincheck/(?P<uidb64>[0-9A-Za-z_\-]+)/$', admincheck ,name='admincheck'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
]