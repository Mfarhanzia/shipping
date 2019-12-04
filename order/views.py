from .import utils
import random, string
from PIL import Image
from decimal import Decimal
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
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from users .models import Photo, WaterMark, SpecUser
from .forms import OrderForm, MaterialQuotationsForm    
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Material, MaterialQuotations, ContainerPricing
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

        email = EmailMessage(subject=mail_subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[
                             to_email], reply_to=(form.cleaned_data['email'],))
        self.send_mail(form.cleaned_data)
        email.content_subtype = "html"
        # email.send(fail_silently=True)
        email.send()
        messages.success(
            self.request, "Your inquiry has been successfully submitted. If you have any questions please email us at info@boltonblock.com.")
        return redirect(self.get_success_url())

    def send_mail(self, form):
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
        email = EmailMessage(subject=mail_subject, body=message,
                             from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
        email.content_subtype = "html"
        email.send()


class ViewOrder(LoginRequiredMixin, UserPassesTestMixin, ListView):
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
        qs = Order.objects.annotate(fieldsum=(Cast('how_much_letter_of_credit', FloatField(
        ))) + (Cast('how_much_line_of_credit', FloatField()))).order_by('-when_to_order', '-fieldsum')
        return qs


@login_required
def order_form(request):
    if request.user.is_superuser:
        pricing = ContainerPricing.objects.all().order_by('id')
        return render(request, "order/form_order.html",{"pricing":pricing})
    elif request.user.specuser.content_permission == True:
        if request.user.specuser.expire_time_spec_content > timezone.now():
            expire_time = request.user.specuser.expire_time_spec_content.timestamp()
            pricing = ContainerPricing.objects.all().order_by('id')
            return render(request, "order/form_order.html", {'title': 'Order Form', 'expire_time': expire_time, "pricing":pricing})
        else:
            user = SpecUser.objects.get(pk=request.user.specuser.id)
            user.content_permission = False
            user.save()
    return render(request, 'users/request_access_content.html')

@login_required
def dealer_view(request):
    try:
        if request.user.specuser.user_type == "dealer":
            qs = SpecUser.objects.filter(
                user_type='homeowner', dealer_no=request.user.specuser.dealer_no)
            return render(request, 'order/dealer_homeowner.html', {'orders': qs, 'title': 'Dealer'})
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/')


@login_required
def view_content(request):
    if request.user.is_superuser:
        return render(request, 'order/structural.html')
    elif request.user.specuser.content_permission == True:
        if request.user.specuser.expire_time_spec_content > timezone.now():
            expire_time = request.user.specuser.expire_time_spec_content.timestamp()
            return render(request, 'order/structural.html', {'title': 'Structural', 'expire_time': expire_time})
        else:
            user = SpecUser.objects.get(pk=request.user.specuser.id)
            user.content_permission = False
            user.save()
    return render(request, 'users/request_access_content.html')

@login_required
def vendor_quotations(request):
    try:
        if request.user.specuser.user_type =="vendor":
            if request.method == 'POST':
                form = MaterialQuotationsForm(request.POST)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.company_name=request.user.specuser.company_name
                    data.material_name=request.POST.get('material_name')
                    data.user_name=f"{request.user.specuser.first_name} {request.user.specuser.last_name}"
                    data.save()
                return redirect("vendor-quotation")
                    
            else:
                form = MaterialQuotationsForm()
                qs = Material.objects.all()
                return render(request, 'order/post_quotation_view.html', {"qs":qs, "title":"Quotation","form":form})
        else:
            return redirect('/')
    except:
        return redirect('/')

@login_required
@user_passes_test(lambda user: user.is_superuser == True, redirect_field_name="/")
def view_quotations(request):
    qs = MaterialQuotations.objects.all()
    return render(request, 'order/view_quotations.html', {"qs":qs, "title":"Quotations"})


def interior_view(request):
    return render(request, 'order/interior.html')


def exterior_view(request):
    return render(request, 'order/exterior.html')
