import random
import string
from order import utils
from django import forms
from datetime import timedelta
from django.conf import settings 
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage 
from .token import account_activation_token
from .models import SpecialUser, Dealer, User
from .forms import SpecialUserForm, EmailListForm
from django.template.loader import render_to_string
from django.contrib.auth import password_validation
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

#views

def home_view(request):
    
    if request.method == "POST":
        form = EmailListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Thanks for Subscribing us')
        else:
            messages.warning(request, f'You have already Subscribed!')

        return redirect('/')
    else:
        form = EmailListForm()
        return render(request, 'users/home.html', {'form': form})

def floor_plan(request):
    return render(request, 'users/floor_plan.html', {'title': 'Floor Plan'})

def specialuser_signup(request):
    """
    this function role: get form data saves it and set user.is_active = False, encrypting user id creating token and sending a link to admin through email 
    """
    if request.user.is_authenticated == False or request.user.is_dealer == True:
        if request.method == 'POST':
            form = SpecialUserForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['user_type'] == 'dealer':
                    email = form.cleaned_data['email']
                    ph = form.cleaned_data['phone_number']
                    fname = form.cleaned_data['f_name']
                    lname = form.cleaned_data['l_name']
                    password = request.POST['password']
                    
                    dealer = Dealer.objects.create(email=email, phone_number=ph, first_name=fname, last_name=lname)
                    dealer.is_active = False
                    dealer.set_password(password)
                    dealer.save()  

                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                if user.company_name:
                    mail_subject = f"New Registration - {user.company_name} by {user.f_name} {user.l_name}'"
                else:
                    mail_subject = f"New Registration - by {user.f_name} {user.l_name}'"
                userid = utils.encrypt(user.pk)     # encrypting user id
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': userid,
                    'token': account_activation_token.make_token(user),
                    })
                to_email = settings.DEFAULT_FROM_EMAIL
                email =EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email],bcc=("farhan71727@gmail.com",), reply_to=(user.email,))
                email.content_subtype = "html"
                
                email.send()
                if user.user_type == 'dealer':
                    messages.success(request, f'Your Request has been sent to Admin for confirmation. You will shortly receive an email on the given email address.We may contact you if we require additional information. Please give us several business days to activate your account.')
                else:
                    messages.success(request, f'Your Request has been sent to Admin for confirmation. You will shortly receive an email on the given email address.')

                return redirect('login')
        else:
            form = SpecialUserForm()
        return render(request, 'users/register.html', {'form': form, 'title': 'Registration'})
    else:
        return redirect('/')

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
        messages.warning(request, f'Activation link is Expired!')
        return redirect('login')

@login_required
@user_passes_test(lambda user: user.is_superuser == True)
def admincheck(request,uidb64):
    """
    This function executes if the link is not expired
    This function role: This func first renders a html page where there is a checkbox
    if admin clicks on it and submit, it gets uidb64(encrypted userid ) from url and decrypt it and set the user state to active, set a activation time and set expiration time, the Special user will get access to the link which will be sent to user in the email(a new email will be sent to the user with link in this function)

    """
    if request.method=="POST":
        if request.POST.get('selector','') == "True":
            # request
            id = utils.decrypt(uidb64)      # decrypting user id
            user = SpecialUser.objects.get(pk=id)
            current_site = get_current_site(request)
            if user.user_type == "dealer":
                dealer = Dealer.objects.get(email = user.email, first_name = user.f_name, last_name = user.l_name )

                all_users = Dealer.objects.all().values_list('dealer_no', flat=True)
                if not dealer.dealer_no:
                    while True:
                        random_number = randomstring()                    
                        if random_number not in all_users:
                            dealer.dealer_no = random_number
                            break
                dealer.is_active = True
                user.dealer_no = dealer.dealer_no
            # current_site = get_current_site(request)
                dealer.content_page_link = f"/view-content/{uidb64}"
                
            user.is_active=True     # setting user to active
            user.activated_on = timezone.now()     #setting activation time
            time = request.POST.get("time")
            user.expire_time = timezone.now() + timedelta(hours=int(time))   #setting expire time
            mail_subject = 'Account Activated.'
            message = render_to_string('users/specialuseremail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uidb64,  
                })
            to_email = user.email
            email =EmailMessage(subject=mail_subject, body=message,from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])

            email.content_subtype = "html"
            email.send()  # sending email with link
            dealer.save()
            user.save()
            if user.company_name:
                messages.success(request, f'You have Given Access to Company {user.company_name} and an email is sent to Company with the access link')
            else:
                messages.success(request, f'You have Given Access to {user.f_name} {user.l_name} and an email is sent to user with the access link.')
            return redirect('register')

        elif request.POST.get('selector','') == "False":
            id = utils.decrypt(uidb64)      # decrypting user id
            try:
                user = get_object_or_404(SpecialUser,pk=id)
                if user.company_name:
                    messages.success(request, f'You have Rejected Access to Company {user.company_name}')
                else:
                    messages.success(request, f'You have Rejected Access to Company {user.f_name} {user.l_name}')
                user.delete()
            except:
                pass
            return redirect('register')       
        else:
            return redirect('/')
    else:
        id = utils.decrypt(uidb64)      # decrypting user id
        try:
            user = SpecialUser.objects.get(pk=id)
        except:
            return redirect('register')
        return render(request, 'users/admincheckuser.html', {'user' : user, 'title': 'Admin Check'})

def randomstring():
    abc=''.join((random.SystemRandom().choice(
        string.digits) for _ in
        range(6)))
    return int(abc)

