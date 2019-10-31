from django.urls import path
from django.conf.urls import url
from .views import (specialuser_signup, activate, admincheck, home_view, floor_plan,
        home_access, models, video_page)
from django.contrib.auth import views as auth_views
    
urlpatterns = [
    path('register/', specialuser_signup ,name='register'),
    path('assembling/', video_page ,name='video-page'),
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

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<req_for>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),

    url(r'^admincheck/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<req_for>[0-9A-Za-z_\-]+)/$', admincheck ,name='admincheck'),

    path('home-access', home_access, name="home-access" ),

    path('models', models, name="models" )
]