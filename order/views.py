import random
import string
from .import utils
from PIL import Image
from .models import Order
from decimal import Decimal
from .forms import OrderForm
from datetime import datetime
from django.db.models import F
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.db.models import FloatField
from django.core.mail import EmailMessage
from django.views.generic import ListView
from django.db.models.functions import Cast
from django.utils.encoding import force_text
from django.views.generic.edit import FormView
from users.token import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users .models import Photo, WaterMark, SpecUser

# Create your views here.

class OrderCreateView(FormView):
    template_name = 'order/order.html'
    form_class = OrderForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context.update({'title': 'Create Order'})
        return context

    def form_valid(self, form):
        
        """If the form is valid, redirect to the supplied URL."""
        form.save()
                
        mail_subject = f"Order Inquiry - {form.cleaned_data['company_name']} by {form.cleaned_data['f_name']} {form.cleaned_data['l_name']}."
        current_site = get_current_site(self.request)
        message = render_to_string('order/order_mail_to_admin.html', {
            'form': form.cleaned_data,
            'domain': current_site.domain,
             })
        to_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email], bcc=("farhan71727@gmail.com",), reply_to = (form.cleaned_data['email'],))
        self.send_mail(form.cleaned_data)
        email.content_subtype = "html"
        # email.send(fail_silently=True)
        email.send()
        messages.success(self.request,"Your inquiry has been successfully submitted. If you have any questions please email us at info@boltonblock.com.")       
        return redirect(self.get_success_url())


    def send_mail(self,form):
        """
        Sending Order Confirm Mail to User 
        """
        current_site = get_current_site(self.request)
        mail_subject = f"Order Confirmation"
        message = render_to_string('order/order_confirm_mail.html', {
            'form': form,
            'domain': current_site.domain
             })
        to_email = form['email']
        email = EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email], bcc=("farhan71727@gmail.com",))
        email.content_subtype = "html"
        email.send()
       
class ViewOrder(LoginRequiredMixin,UserPassesTestMixin,ListView):
    """
    view for showing orders for authenticated users
    """
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    model = Order
    template_name = 'order/view_orders.html'  
    context_object_name = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super(ViewOrder, self).get_context_data(**kwargs)
        context.update({'title': 'Orders'})
        return context
    
    def get_queryset(self):
        """ 
        overriding queryset for ranking the orders
        """
        qs = Order.objects.annotate(fieldsum=(Cast('how_much_letter_of_credit',FloatField())) + (Cast('how_much_line_of_credit',FloatField()))).order_by('-when_to_order', '-fieldsum')
        return qs
    

@login_required
def view_content(request):
    if request.user.is_superuser:
        return render(request, 'order/structural.html')
    elif request.user.specuser.content_permission == True:
        if request.user.specuser.expire_time_spec_content > timezone.now():
            return render(request, 'order/structural.html')
        else:
            user = SpecUser.objects.get(pk=request.user.specuser.id)
            user.content_permission = False
            user.save()
    else:
        return render(request, 'users/request_access_content.html')