import json, base64
from io import BytesIO
from datetime import date
from xhtml2pdf import pisa
from django.conf import settings
from django.utils import timezone
from users .models import SpecUser
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import FloatField
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.db.models.functions import Cast
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from formtools.wizard.views import SessionWizardView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Order, Material, MaterialQuotations, ContainerPricing, CartOrder, CustomContainerPricing
from .forms import (BuyerAppForm, BuyerAppForm2, MaterialQuotationsForm, AddCustomProductForm, UserTermsForm,
                    DeliveryInfoForm, LoginForm)
from .cart import Cart
# Create your views here.


class ViewBuyerApp(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    view for showing Buyer Application for admin
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
        context = super(ViewBuyerApp, self).get_context_data(**kwargs)
        context.update({'title': 'Orders'})
        return context

    def get_queryset(self):
        """ 
        overriding queryset for ranking the orders
        """
        qs = Order.objects.annotate(fieldsum=(Cast('how_much_letter_of_credit', FloatField(
        ))) + (Cast('how_much_line_of_credit', FloatField()))).order_by('-when_to_order', '-fieldsum')
        return qs


class OrderForm(SessionWizardView):
    # file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    form_list = [AddCustomProductForm, BuyerAppForm, DeliveryInfoForm, BuyerAppForm2, UserTermsForm, LoginForm,
                 AddCustomProductForm]

    def check_user_authentication(self):
        if self.request.user.is_authenticated == True:
            return False
        else:
            return True

    def get_template_names(self):
        """
        Return the template name for the current step
        """
        templates = {
        0: 'order/form_order.html',
        1: 'order/buyer_app_form.html',
        2: 'order/delivery_info.html',
        3: 'order/buyer_app_form.html',
        4: 'order/order_terms.html',
        5: 'order/form_wizard_login.html',
        6: 'order/review_order.html',
       }
        return [templates[int(self.steps.current)]]

    def save_cart(self, form2, buyer_app, delivery_info):
        """saving the container orders"""

        cart = Cart(self.request).cart
        print_name = form2.cleaned_data["print_name"]
        regular_order_ids = []
        custom_order_id = None
        image=None
        try:
            format, imgstr = form2.cleaned_data["image_field"].split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 
        except Exception as e:
            print(";;;;;;;;;;;  ERROR  ;;;;",e)
            pass
        for key in cart:
            data = cart[key]
            if "width" in data.keys():
                product = get_object_or_404(CustomContainerPricing, id=key)
                custom_order_obj = CartOrder(
                    user_id= self.request.user.id,
                    delivery_info_obj= delivery_info,
                    buyer_app_obj= buyer_app,
                    custom_order= product,
                    custom_floors= data["no_of_floors"],
                    custom_width= data["width"],
                    custom_depth= data["depth"],
                    quantity= data["quantity"],
                    furnishing_option= data["furnishing_option_custom"],
                )
                if image != None:
                    custom_order_obj.user_image = image
                custom_order_obj.save()
                custom_order_id = custom_order_obj.id

            else:
                product = get_object_or_404(ContainerPricing, id=key)
                current_order = CartOrder(
                    user_id=self.request.user.id,
                    delivery_info_obj=delivery_info,
                    buyer_app_obj=buyer_app,
                    order_items=product,
                    quantity=data["quantity"],
                    furnishing_option=data["furnished_option"],
                )
                if image != None:
                    current_order.user_image = image
                current_order.save()
                regular_order_ids.append(int(current_order.id))
        return self.create_order_pdf(print_name, custom_order_id, regular_order_ids)

    @staticmethod
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

    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=self.fetch_resources, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf'), result.getvalue()
        return None

    def send_mail_PDF(self,template,context,mail):
        html = template.render(context)
        pdf,pdf2 = self.render_to_pdf('order/order_pdf.html', context)
        ###sending email with attachment(pdf)    
        mail_subject = f"Shipping Container Homes Order Detail"
        if mail == settings.DEFAULT_FROM_EMAIL:
            msg = f"Hi Admin,\n A new order is Placed by {context['print_name']}. \n\n Order Receipt is attached."
            email = EmailMessage(subject=mail_subject, body=msg, from_email=settings.DEFAULT_FROM_EMAIL, to=(mail,),)
            email.attach('order_details.pdf', pdf2 , 'application/pdf')
        else:
            user_msg = f"Hi {context['print_name']},\n Thanks for Ordering at BoltonBloks.\n\n Your Receipt is attached."
            email = EmailMessage(subject=mail_subject, body=user_msg, from_email=settings.DEFAULT_FROM_EMAIL, to=(mail,),)
            email.attach(f"{context['print_name']}.pdf", pdf2 , 'application/pdf')
        email.encoding = 'us-ascii'
        email.send()
    
    def create_order_pdf(self, print_name, custom_order_id, regular_order_ids):
        template = get_template('order/order_pdf.html')
        try:
            cart = CartOrder.objects.filter(id__in=regular_order_ids)
        except Exception as e:
            cart = ""
        ## custom order
        try:
            custom_order_obj = CartOrder.objects.get(id=int(custom_order_id))
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
            return "no order"

        total = Cart(self.request).get_total_price()
        context = {
            "custom_order_obj":custom_order_obj,
            "cart": cart,
            "date":date_,
            "total":total,
            "user_image": user_image,
            "print_name" : print_name,
            "delivery_date": self.get_cleaned_data_for_step('2')['delivery_date'],
            }  
        ##admin
        pdf = self.send_mail_PDF(template,context,settings.DEFAULT_FROM_EMAIL)

        context = {
            "custom_order_obj":custom_order_obj,
            "cart": cart,
            "date":date_,
            "total":total,
            "print_name" : print_name,
            "user_image": None,
            "delivery_date": self.get_cleaned_data_for_step('2')['delivery_date'],
            }  
        pdf = self.send_mail_PDF(template,context,user_mail)
        messages.success(self.request,"Order Received.\nYour Receipt is Sent to Your Email Address.")

    def get_form_step_data(self, form):
        print("get_form_step_data", self.steps.step1)
        data = super().get_form_step_data(form)
        # if self.steps.step1 == 1:
        #     self.form1_data = self.request.session["form_1_data"] ={}
            # self.form1_data["quantity"] = self.request.POST.getlist('quantity')
            # self.form1_data["furnishing_option"] = self.request.POST.getlist('furnishing_option')
            # self.form1_data["custom_order"] = self.request.POST
        if self.steps.step1 == 6:
            self.form1_data = self.request.session["form_1_data"] = {}
            email = data.get("5-email")
            password= data.get("5-password")
            self.request.session["user_credentials"] = {"email":email,"password":password}

        return data

    def render(self, form=None, *args,**kwargs):
        if self.steps.step1 == 7:
            if self.request.POST.get("2-accept") == "decline":
                self.storage.reset()
                self.request.session["form_1_data"] = ""
                cart = Cart(self.request)
                cart.clear()
                return redirect("order-form")
        try:
            iscart = self.request.session["cart"]
        except:
            iscart = None
        if self.steps.step1 > 1 and not iscart:
            return redirect("order-form")

        return super(OrderForm, self).render(form, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(OrderForm, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 1:
            Cart(self.request).clear()
            form2 = AddCustomProductForm()
            pricing = ContainerPricing.objects.all().order_by('id')
            custom_pricing = CustomContainerPricing.objects.all().first()
            context.update({
                "pricing":pricing,
                "form2":form2,
                'title': 'Order',
                "quantity": range(300),
                "custom_pricing":custom_pricing,
                })
        elif self.request.user.is_authenticated and self.steps.step1 == 6:
            print("im runing6")
            context = self.update_context(context)
        elif self.steps.step1 == 7:
            print("im runing7")
            context = self.update_context(context)
        return context

    def update_context(self, context):
        """This is a custom function not form_wizard"""
        cart_obj = Cart(self.request)
        regular_order = cart_obj.cart
        custom_order = None
        for key in cart_obj.cart:
            data = cart_obj.cart[key]
            if "width" in data.keys():
                custom_order = cart_obj.cart[key]
        context.update({
            "order": regular_order,
            "custom_order": custom_order,
            "total": cart_obj.get_total_price(),
            'shipping_info': self.get_cleaned_data_for_step('2'),
            'buyer_info': self.get_cleaned_data_for_step('3'),
            'buyer_app1': BuyerAppForm(self.get_cleaned_data_for_step('1')),
        })
        return context

    def done(self, form_list, **kwargs):
        email = self.request.session["user_credentials"]["email"]
        password = self.request.session["user_credentials"]["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        forms = list(form_list)
        delivery_info_form = forms[2]
        delivery_info = delivery_info_form.save()
        buyer_app = Order(user=self.request.user)
        buyer_form = forms[1]
        buyer_form2 = forms[3]
        for form in [buyer_form,buyer_form2]:
            for field_name, value in form.cleaned_data.items():
                setattr(buyer_app, field_name, value)
        buyer_app.save()
        order_status = self.save_cart(forms[4], buyer_app, delivery_info)
        self.request.session["form_1_data"] = ""
        # print("done===",self.request.session.items())
        Cart(self.request).clear()
        if order_status != "no order":
            return redirect("/")
        else:
            messages.warning(self.request, "You must select something to place an order!")
        return redirect("order-form")


@require_POST
def add_order(request):
    cart = Cart(request)
    is_custom = request.POST.get("custom_quantity", None)
    if is_custom:
        cus_qty = int(is_custom.split("##")[0])
        custom_order_id = int(is_custom.split("##")[1])
        no_of_floors = request.POST['no_of_floors']
        width = request.POST['width']
        depth = request.POST['depth']
        furnishing_option_custom = request.POST['furnishing_option_custom']
        product = CustomContainerPricing.objects.get(id=custom_order_id)
        area = (int(no_of_floors) * int(width) * int(depth))
        if cus_qty > 20 or area > 20:
            price = (area * cus_qty) * product.custom_price21
        else:
            price = (area * cus_qty) * product.custom_price
        price = int(price)
        cart.add_custom(no_of_floors, cus_qty, width, depth, furnishing_option_custom, product, price)
    else:
        quantity = int(request.POST["quantity"].split("##")[0])
        order_id = request.POST["quantity"].split("##")[1]
        furnishing_option = request.POST["furnishing_option"]
        product = ContainerPricing.objects.get(id=order_id)
        if quantity > 20:
            price = product.price21
        else:
            price = product.price
        price = int(price)
        cart.add(quantity, furnishing_option, product, price)
    cart_items = request.session['cart']
    print(">>>Cart: {}".format(len(cart_items)),cart_items)
    total = cart.get_total_price()
    return JsonResponse(total, safe=False)


@require_POST
def remove_order(request, pk):
    cart = Cart(request)
    cart.remove(pk)
    total = cart.get_total_price()
    return JsonResponse(total, safe=False)


@login_required
@user_passes_test(lambda user: user.is_superuser == True, redirect_field_name="/")
def view_container_orders(request):
    all_orders = CartOrder.objects.all()
    return render(request, "order/view_container_orders.html", {"orders":all_orders})


@login_required
def view_container_order_items(request, pk=None):
    if request.user.is_superuser:
        items = CartOrder.objects.filter(user=pk)
    else:
        items = CartOrder.objects.filter(user=request.user)
    # return render(request, "order/view_container_order_items.html", {"items":items})
    return render(request, "order/order-history.html", {"items":items})


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
def view_3d_model(request):
    """3d view of container home models"""
    return render(request, "order/3story2w_3dmodel.html")


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