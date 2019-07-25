from datetime import timedelta
from django.utils import timezone
from django.conf import settings 
from order import utils
from .models import SpecialUser
from .forms import SpecialUserForm
from django.contrib import messages
from django.core.mail import EmailMessage 
from .token import account_activation_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#views


def home_view(request):
    return render(request, 'users/home.html')


def specialuser_signup(request):
    """
    this function role: get form data saves it and set user.is_active = False, encrypting user id creating token and sending a link to admin through email 
    """

    if request.method == 'POST':
        form = SpecialUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account Activation Requested.'
            userid = utils.encrypt(user.pk)     # encrypting user id
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': userid,
                'token':account_activation_token.make_token(user),
                })
            to_email = "bilalvasl@gmail.com"
            # email =EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email],bcc=("farhan71727@gmail.com",))
            email =EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email],bcc=("farhan71727@gmail.com",))
            email.content_subtype = "html"
            # email.send(fail_silently=True)
            email.send()
            messages.success(request, f'Your Request has been sent to Admin for confirmation. You will shortly receive an email on the given email address.')
            return redirect('login')
    else:
        form = SpecialUserForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Registration'})

def activate(request, uidb64, token):
    """
    When user clicks on the link this function gets uidb64(encrypted user id) and token
    if link is valid the function in If condition is called 
    """
    try:
        uid = utils.decrypt(uidb64)         # decrypting user id
        user = SpecialUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, SpecialUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
      return redirect ('admincheck', uidb64)      
    else:
        messages.warning(request, f'Activation link is invalid!')
        return redirect('login')

@login_required
def admincheck(request,uidb64):
    """
    This function executes if the link is not expired
    This function role: This func first renders a html page where there is a checkbox
    if admin clicks on it and submit, it gets uidb64(encrypted userid ) from url and decrypt it and set the user state to active, set a activation time and set expiration time, the Special user will get access to the link which will be sent to user in the email(a new email will be sent to the user with link in this function)

    """
    if request.method=="POST":
        if request.POST.get('checkbox','') == "True":
            
            id = utils.decrypt(uidb64)      # decrypting user id
            user = SpecialUser.objects.get(pk=id)

            user.is_active=True     # setting user to active
            user.activated_on = timezone.now()     #setting activation time
            user.expire_time = timezone.now() + timedelta(hours=12)   #setting expire time

            current_site = get_current_site(request)
            mail_subject = 'Account Activated.'
            message = render_to_string('users/specialuseremail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uidb64,  
                })
            to_email = user.email
            email =EmailMessage(subject=mail_subject, body=message,from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])

            email.content_subtype = "html"
            email.send(fail_silently=True)  # sending email with link

            user.save()
            messages.success(request, f'You have Given Access to Company {user.company_name} and an email is sent to Company with the access link')
            return redirect('register')
        else:
            return redirect('/')
    else:
        id = utils.decrypt(uidb64)      # decrypting user id
        user = SpecialUser.objects.get(pk=id)
        return render(request, 'users/admincheckuser.html', {'user' : user, 'title': 'Admin Check'})
        