from .import utils
from PIL import Image
from decimal import Decimal
from datetime import date
import random, string, json, base64, os
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
from django.contrib.sites.shortcuts import get_current_site
from .forms import OrderForm, MaterialQuotationsForm, AddCustomProductForm  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Order, Material, MaterialQuotations, ContainerPricing, CartOrder, CustomContainerPricing
from django.views.decorators.http import require_POST

from xhtml2pdf import pisa
from django_xhtml2pdf.utils import generate_pdf
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from django.http import JsonResponse
from django.core.files.base import ContentFile


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
    """ order form without permission"""
    form2 = AddCustomProductForm()
    pricing = ContainerPricing.objects.all().order_by('id')
    custom_pricing = CustomContainerPricing.objects.all()[0]
    context = {"pricing":pricing,
     "form2":form2,
     'title': 'Order',
     "quantity": range(50),
     "custom_pricing":custom_pricing,
     }
    return render(request, "order/form_order.html", context)


def add_order(request, pk=None):
    """adding container order to session"""
    quantities = request.GET.getlist('quantity')
    dates = request.GET.getlist('date_')
    no_of_floors = request.GET['no_of_floors']
    width = request.GET['width']
    depth = request.GET['depth']
    cus_qty = request.GET['custom_quantity']
    cus_date = request.GET['custom_date']
    total = 0
    for q,d in zip(quantities,dates):
        if q == "" or d == "":
            continue
        qty = int(q.split("##")[0]) 
        pk = int(q.split("##")[1]) 
        
        product = get_object_or_404(ContainerPricing, id=pk)
        if qty > 20:
            total += qty * product.price21     
        else:
            total += qty * product.price     
    if (no_of_floors != "" and width != "" and depth != "" and cus_qty !='' and cus_date != ""):
        qty = int(cus_qty.split("##")[0]) 
        pk = int(cus_qty.split("##")[1])      
        product = get_object_or_404(CustomContainerPricing, id=pk)
        if qty > 20:
            total += qty * product.custom_price21 
        else:
            total += qty * product.custom_price 
    return JsonResponse(total, safe=False)


@require_POST
def save_cart(request):
    """saving the container orders"""
    quantities = request.POST.getlist('quantity')
    dates = request.POST.getlist('date_')

    request.session['print_name'] = request.POST['print_name']
    no_of_floors = request.POST['no_of_floors']
    width = request.POST['width']
    depth = request.POST['depth']
    cus_qty = request.POST['custom_quantity']
    cus_date = request.POST['custom_date']
    request.session['custom_id']=''
    request.session['list_ids']=''
    order_ids = []
    image=None
    try:
        format, imgstr = request.POST['webcam'].split(';base64,') 
        ext = format.split('/')[-1]
        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 
    except Exception as e:
        pass
        # print("}}}}}}}}}}}",e) 
        
    for q,date in zip(quantities,dates):
        if q == "" or date == "":
            continue
        qty = int(q.split("##")[0]) 
        pk = int(q.split("##")[1]) 
        product = get_object_or_404(ContainerPricing, id=pk)
        
        current_order = CartOrder(
        user_id=request.user.id,
        order_items = product,
        quantity = qty, 
        delivery_date = date.replace('"',''),
        )
        if image != None:

            current_order.user_image = image
        current_order.save()
        order_ids.append(int(current_order.id))

    if (no_of_floors != "" and width != "" and depth != "" and cus_qty !='' and cus_date != ""):
        qty = int(cus_qty.split("##")[0]) 
        pk = int(cus_qty.split("##")[1])      
        product = get_object_or_404(CustomContainerPricing, id=pk)
        custom_order_obj = CartOrder(
        user_id=request.user.id,
        custom_order = product,
        custom_floors = no_of_floors,
        custom_width = width,
        custom_depth = depth,
        quantity = qty, 
        delivery_date = cus_date.replace('"',''),
        )
        if image != None:
            custom_order_obj.user_image = image
        custom_order_obj.save()
        request.session['custom_id'] = custom_order_obj.id
    request.session['list_ids'] = json.dumps(order_ids)
    return redirect("order-pdf")

def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    # path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_ROOT, "/"))
    # path = os.path.join(rel, uri)
    # print("path",path)
    return uri 

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources, encoding="UTF-8")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf'), result.getvalue()
    return None


def send_mail_PDF(template,context,mail):
    html = template.render(context)
    pdf,pdf2 = render_to_pdf('order/order_pdf.html', context)
    ###sending email with attachment(pdf)    
    mail_subject = f"Shipping Container Homes Order Detail"
    to_email = settings.DEFAULT_FROM_EMAIL
    # to_email = "farhan71727@gmail.com"
    email = EmailMessage(subject=mail_subject, body="Order Detail", from_email=settings.DEFAULT_FROM_EMAIL, to=(mail,),)
    email.attach('order_details.pdf', pdf2 , 'application/pdf')
    email.encoding = 'us-ascii'
    email.send()
    

def create_order_pdf(request):
    template = get_template('order/order_pdf.html')
    total = 0
    try:
        ids = json.loads(request.session['list_ids'])
        cart = CartOrder.objects.filter(id__in=ids)
        
        for data in cart:
            if data.quantity >20:
                total += data.quantity * data.order_items.price21 
            else:
                total += data.quantity * data.order_items.price 
    except Exception as e:
        cart = ""

    ## custom order
    try:
        custom_id = request.session['custom_id']
        custom_order_obj = CartOrder.objects.get(id=int(custom_id))
        if custom_order_obj.quantity >20:
            total += custom_order_obj.quantity * custom_order_obj.custom_order.custom_price21 
        else:
            total += custom_order_obj.quantity * custom_order_obj.custom_order.custom_price 
    except:
        custom_order_obj = ""
    date_ = date.today()
    try:
        try:
            user_mail = cart[0].user.email
            user_image = cart[0].user_image.path
        except:
            user_image = custom_order_obj.user_image.path
            user_mail = custom_order_obj.user.email
    except Exception as e:
        print("no user found",e)
        return redirect("order-form")
    context = {
        "custom_order_obj":custom_order_obj,
        "cart": cart,
        "date":date_,
        "total":total,
        "user_image": user_image,
        "print_name" : request.session['print_name']
        }  
    ##admin
    pdf = send_mail_PDF(template,context,settings.DEFAULT_FROM_EMAIL)
    # html = template.render(context)
    # pdf,pdf2 = render_to_pdf('order/order_pdf.html', context)
    # ###sending email with attachment(pdf)    
    # mail_subject = f"Shipping Container Homes Order Detail"
    # to_email = settings.DEFAULT_FROM_EMAIL
    # # to_email = "farhan71727@gmail.com"
    # email = EmailMessage(subject=mail_subject, body="Order PDF", from_email=settings.DEFAULT_FROM_EMAIL, to=([to_email],),)
    # email.attach('order_details.pdf', pdf2 , 'application/pdf')
    # email.encoding = 'us-ascii'
    # email.send()

    context = {
        "custom_order_obj":custom_order_obj,
        "cart": cart,
        "date":date_,
        "total":total,
        "print_name" : request.session['print_name'],
        "user_image": None,
        }  
    pdf = send_mail_PDF(template,context,user_mail)
    ##user
    # html = template.render(context)
    # pdf,pdf2 = render_to_pdf('order/order_pdf.html', context)
    # ###sending email with attachment(pdf)    
    # mail_subject = f"Shipping Container Homes Order Detail"
    # to_email = settings.DEFAULT_FROM_EMAIL
    # # to_email = "farhan71727@gmail.com"
    # email = EmailMessage(subject=mail_subject, body="Order PDF", from_email=settings.DEFAULT_FROM_EMAIL, to=(user_mail,),)
    # email.attach('order_details.pdf', pdf2 , 'application/pdf')
    # email.encoding = 'us-ascii'
    # email.send()
    messages.success(request,"Order Received.\nYour Receipt is Sent to Your Email Address")
    return redirect("/")


@login_required
@user_passes_test(lambda user: user.is_superuser == True, redirect_field_name="/")
def view_container_orders(request):
    all_orders = CartOrder.objects.all()
    return render(request, "order/view_container_orders.html", {"orders":all_orders})


@login_required
@user_passes_test(lambda user: user.is_superuser == True, redirect_field_name="/")
def view_container_order_items(request, pk):
    items = CartOrder.objects.filter(user=pk)
    return render(request, "order/view_container_order_items.html", {"items":items})


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
def view_struc_drawings(request):
    """structural_drawings"""
    if request.user.is_superuser:
        return render(request, 'order/structural.html',{'title': 'Structural Drawings',})
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
def view_arc_drawings(request):
    """architectural_drawings"""
    if request.user.is_superuser:
        return render(request, 'order/architectural_drawings.html',{'title': 'Architectural Drawings'})
    elif request.user.specuser.content_permission == True:
        if request.user.specuser.expire_time_spec_content > timezone.now():
            expire_time = request.user.specuser.expire_time_spec_content.timestamp()
            return render(request, 'order/architectural_drawings.html', {'title': 'Architectural Drawings', 'expire_time': expire_time})
        else:
            user = SpecUser.objects.get(pk=request.user.specuser.id)
            user.content_permission = False
            user.save()
    return render(request, 'users/request_access_content.html')


@login_required
def view_report_sap(request):
    """Report FEA SAP"""
    if request.user.is_superuser:
        return render(request, 'order/report_sap_pdfs.html',{'title': 'Report FEA SAP'})
    elif request.user.specuser.content_permission == True:
        if request.user.specuser.expire_time_spec_content > timezone.now():
            expire_time = request.user.specuser.expire_time_spec_content.timestamp()
            return render(request, 'order/report_sap_pdfs.html', {'title': 'Report FEA SAP', 'expire_time': expire_time})
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
