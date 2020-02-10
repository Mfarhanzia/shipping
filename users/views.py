import random
import string
from order import utils
from django import forms
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .models import User, SpecUser, UserPreferences
from django.contrib import messages
from django.core.mail import EmailMessage
from .token import account_activation_token
from .forms import EmailListForm, SpecUserForm, ContactUsForm, RegistrationForm1, RegistrationForm2, UserPreferencesForm
from django.template.loader import render_to_string
from django.contrib.auth import password_validation
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from formtools.wizard.views import CookieWizardView
# views


class RegistrationForm(CookieWizardView):
    form_list = [RegistrationForm1, RegistrationForm2, UserPreferencesForm]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super(RegistrationForm, self).get(request, *args, **kwargs)

    def get_template_names(self):
        """
        Return the template name for the current step
        """
        templates = {
        0: 'users/signup.html',
        1: 'users/signup.html',
        2: 'users/user_preference.html',
       }
        return [templates[int(self.steps.current)]]
    
    def send_mail(self,user):
        print("user_id", user.pk)
        current_site = get_current_site(self.request)
        if user.user_type == "dealer":
            last_obj = SpecUser.objects.all().last()
            last_id = last_obj.pk
            dealer_no = ''.join((random.SystemRandom().choice(string.digits) for _ in range(5)))
            user.dealer_no = dealer_no+str(last_id)
            user.save()
        current_site = get_current_site(self.request)
        mail_subject = f"Sign Up Successful."
        message = render_to_string('users/sign_up_mail.html', {
                'user': user,
                'domain': current_site.domain,
                })
        to_email = user.email
        email = EmailMessage(subject=mail_subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email], reply_to=(settings.DEFAULT_FROM_EMAIL,))
        email.content_subtype = "html"
        try:
            email.send()
        except:
            messages.error(self.request, f'Something went Wrong!. Please Try again.')
            return redirect(self.request.path_info)
        
        if user.user_type == "dealer":
            messages.success(self.request, f'Sign Up Successful! Your Dealer Number is sent to your provided email.')
        else:
            messages.success(self.request, f'Sign Up Successful!')

    def done(self, form_list, **kwargs):
        user = SpecUser()
        user_pref = UserPreferences()
        for form in form_list:
            for field_name, value in form.cleaned_data.items():
                if "password1" in field_name:
                    user.set_password(value)
                setattr(user, field_name, value)
                setattr(user_pref, field_name, value)
        user.content_permission = False
        user.home_permission = False
        user.save()
        user_pref.user_obj = user
        user_pref.save()
        self.send_mail(user)
        return redirect('login')


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
        return render(request, 'users/home.html')


def concept_page(request):
    return render(request, "users/concept.html")


def amenities(request):
    return render(request, "users/amenities.html")


def models(request):
    return render(request, 'users/models.html')


def electric_cars_view(request):
    return render(request, 'users/electric_cars.html')


def electric_cars_exterior_view(request):
    return render(request, 'users/car_exterior.html')


def electric_cars_interior_view(request):
    return render(request, 'users/car_interior.html')

@login_required
def floor_plan(request):
    return render(request, 'users/floor_plan.html', {'title': 'Floor Plan'})
    
@login_required
@user_passes_test(lambda user: user.is_superuser != True, redirect_field_name="/")
def home_access(request):
    """
    this function role: get form data saves it and set user.is_active = False, encrypting user id creating token and sending a link to admin through email 
    """

    if request.method == 'POST':
        req_for = request.POST['req-access']
        req_for = utils.encrypt(req_for)
        user = request.user.specuser
        current_site = get_current_site(request)
        if user.company_name:
            mail_subject = f"Access Request - {user.company_name} by {user.first_name} {user.last_name}'"
        else:
            mail_subject = f"Access Request - by {user.first_name} {user.last_name}'"
        userid = utils.encrypt(user.pk)     # encrypting user id
        token_arg = [user, utils.decrypt(req_for)]
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': userid,
            'req_for': req_for,
            'token': account_activation_token.make_token(token_arg),
        })
        to_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(subject=mail_subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email], reply_to=(user.email,))
        email.content_subtype = "html"
        try:
            email.send()
        except Exception as e:
            messages.error(request, f'Something went Wrong!. Please Try again.')
            return redirect(request.path_info)
        messages.success(
            request, f'Your Request has been sent to Admin for confirmation. You will shortly receive an email on the given email address.')

        return redirect('login')
    else:
        return redirect('/')


def activate(request, uidb64, req_for, token):
    """
    When user clicks on the link this function gets uidb64(encrypted user id) and token
    if link is valid the function in If condition is called 
    """
    try:
        uid = utils.decrypt(uidb64)         # decrypting user id
        user = SpecUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, SpecUser.DoesNotExist):
        user = None
    token_arg = [user, utils.decrypt(req_for)]
    if user is not None and account_activation_token.check_token(token_arg, token):
        return redirect('admincheck', uidb64, req_for)
    else:
        messages.warning(request, f'Link is Expired!')
        return redirect('login')


@login_required
@user_passes_test(lambda user: user.is_superuser == True, redirect_field_name="/")
def admincheck(request, uidb64, req_for):
    """
    This function executes if the link is not expired
    This function role: This func first renders a html page where there is a checkbox
    if admin clicks on it and submit, it gets uidb64(encrypted userid ) from url and decrypt it and set a activation time and set expiration time, the Special user will get access to the link which will be sent to user in the email(a new email will be sent to the user with link in this function)
    """
    try:
        if request.method == "POST":
            if request.POST.get('selector', '') == "True":

                id = utils.decrypt(uidb64)      # decrypting user id
                user = SpecUser.objects.get(pk=id)
                current_site = get_current_site(request)
                req_for = utils.decrypt(req_for)
                if 'home' in req_for:
                    # giving access to view home
                    user.home_permission = True
                    user.activation_time_home = timezone.now()
                    time = request.POST.get("time")
                    user.expire_time_home = timezone.now() + timedelta(hours=int(time))

                elif 'content' in req_for:
                    # giving access to view content
                    user.content_permission = True
                    user.activation_time_spec_content = timezone.now()
                    time = request.POST.get("time")
                    user.expire_time_spec_content = timezone.now() + timedelta(hours=int(time))

                mail_subject = 'Access Granted.'
                message = render_to_string('users/specialuseremail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'req_for': req_for,
                    'time': int(time)
                })
                to_email = user.email
                email = EmailMessage(subject=mail_subject, body=message,
                                     from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])

                email.content_subtype = "html"
                email.send()  # sending email with link

                user.save()
                if user.company_name:
                    messages.success(
                        request, f'You have Given Access to Company {user.company_name} and an email is sent to Company with the access link')
                else:
                    messages.success(
                        request, f'You have Given Access to {user.first_name} {user.last_name} and an email is sent to user.')
                return redirect('register')

            elif request.POST.get('selector', '') == "False":
                id = utils.decrypt(uidb64)      # decrypting user id
                try:
                    user = get_object_or_404(SpecUser, pk=id)
                    if user.company_name:
                        messages.success(
                            request, f'You have Rejected Access to Company {user.company_name}')
                    else:
                        messages.success(
                            request, f'You have Rejected Access to {user.first_name} {user.last_name}')
                except:
                    pass
                return redirect('register')
            else:
                return redirect('/')
        else:
            id = utils.decrypt(uidb64)      # decrypting user id
            req_for = utils.decrypt(req_for)
            try:
                user = SpecUser.objects.get(pk=id)
            except:
                return redirect('register')
            return render(request, 'users/admincheckuser.html', {'user': user, 'title': 'Admin Check', 'req_for': req_for})
    except Exception as e:
        print(e)
        messages.error(request, f'Something went Wrong!{e}')
        return redirect(request.path_info)


@login_required
def video_page(request):
    return render(request, "order/video.html", {"title":"Assembling"})


def contact_view(request):
    form = ContactUsForm()
    if request.method=="POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            messages.success(request,"Message Sent!")
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            message = render_to_string('users/user_message.html', {
            'user_name': f"{first_name} {last_name}",
            "message": message,
            })
            email =EmailMessage(subject,message, to=[settings.DEFAULT_FROM_EMAIL], reply_to=(email,))
        email.content_subtype = "html"
        email.send()
        messages.success(request,"Message Sent!")
        return redirect('contact-us')
    return render(request, "users/contact_us.html", {"form":form})

