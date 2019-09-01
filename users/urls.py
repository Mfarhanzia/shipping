from django.urls import path
from django.conf.urls import url
from .views import specialuser_signup, activate, admincheck, home_view, floor_plan
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', specialuser_signup ,name='register'),
    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
              email_template_name = 'users/password_reset_email.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
         
    path('', home_view, name="home"),
    
    path('floor-plan', floor_plan, name="floor_plan"),

    url(r'^admincheck/(?P<uidb64>[0-9A-Za-z_\-]+)/$', admincheck ,name='admincheck'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
]