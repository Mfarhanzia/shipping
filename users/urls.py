from django.urls import path
from django.conf.urls import url
from .views import (concept_page, specialuser_signup, activate, admincheck, home_view, floor_plan,
        home_access, models, video_page, electric_cars_view,electric_cars_exterior_view,
        electric_cars_interior_view, contact_view, RegistrationForm)
from django.contrib.auth import views as auth_views
from .forms import RegistrationForm1, RegistrationForm2  

urlpatterns = [
    path('electric-cars/exterior', electric_cars_exterior_view ,name='cars-exterior'),
    path('electric-cars/interior', electric_cars_interior_view ,name='cars-interior'),
    path('electric-cars/', electric_cars_view ,name='electric-cars'),
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
    path('models', models, name="models"),
    path('concept', concept_page, name="concept"),
    path('contactus', contact_view, name="contact-us"),

    # path('signup/', RegistrationForm.as_view([RegistrationForm1, RegistrationForm2]), name="sign-up"),
    path('signup/', RegistrationForm.as_view(), name="sign-up"),
]