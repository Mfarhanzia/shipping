from datetime import date
import json, base64
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.db.models import FloatField
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.db.models.functions import Cast
from users .models import SpecUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import BuyerAppForm, MaterialQuotationsForm, AddCustomProductForm, UserTermsForm
from .models import Order, Material, MaterialQuotations, ContainerPricing, CartOrder, CustomContainerPricing
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.http import JsonResponse
from django.core.files.base import ContentFile
from formtools.wizard.views import SessionWizardView
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


class OrderForm(LoginRequiredMixin, SessionWizardView):
   
    # file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    form_list = [AddCustomProductForm, BuyerAppForm, UserTermsForm,AddCustomProductForm]
    def get_template_names(self):
        """
        Return the template name for the current step
        """
        # self.request.session.clear()
        templates = {
        0: 'order/form_order.html',
        1: 'order/buyer_app_form.html',
        2: 'order/order_terms.html',
        3: 'order/review_order.html',
       }
        return [templates[int(self.steps.current)]]
        
    def save_cart(self, form2):
        """saving the container orders"""
        # print("===saving=======", form2.cleaned_data)
        form1_data = self.request.session["form_1_data"]
        quantities = form1_data['quantity'] # list
        dates = form1_data['date_'] # list
        form1_data['print_name'] = form2.cleaned_data["print_name"]
        no_of_floors = form1_data["custom_order"]['no_of_floors']
        width = form1_data["custom_order"]['width']
        depth = form1_data["custom_order"]['depth']
        cus_qty = form1_data["custom_order"]['custom_quantity']
        cus_date = form1_data["custom_order"]['custom_date']
        self.request.session["form_1_data"]['custom_id']=''
        self.request.session["form_1_data"]['list_ids']=''
        order_ids = []
        image=None
        try:
            format, imgstr = form2.cleaned_data["image_field"].split(';base64,') 
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 
        except Exception as e:
            print(";;;;;;;;;;;  ERROR  ;;;;",e)
            pass

        for q,date in zip(quantities,dates):
            if q == "" or date == "":
                continue
            qty = int(q.split("##")[0]) 
            pk = int(q.split("##")[1]) 
            product = get_object_or_404(ContainerPricing, id=pk)
            current_order = CartOrder(
            user_id=self.request.user.id,
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
            user_id=self.request.user.id,
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
            self.request.session["form_1_data"]['custom_id'] = custom_order_obj.id
        self.request.session["form_1_data"]['list_ids'] = json.dumps(order_ids)
        return self.create_order_pdf()

    def fetch_resources(self,uri, rel):
        """
        Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
        `uri` is the href attribute from the html link element.
        `rel` gives a relative path, but it's not used here.
        """
        # path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_ROOT, "/"))
        # path = os.path.join(rel, uri)
        # print("path",path)
        return uri 

    def render_to_pdf(self,template_src, context_dict={}):
        template = get_template(template_src)
        html  = template.render(context_dict)
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
    
    def create_order_pdf(self):
        template = get_template('order/order_pdf.html')
        total = 0
        try:
            ids = json.loads(self.request.session["form_1_data"]['list_ids'])
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
            custom_id = self.request.session["form_1_data"]['custom_id']
            custom_order_obj = CartOrder.objects.get(id=int(custom_id))
            area = (int(custom_order_obj.custom_floors) * int(custom_order_obj.custom_width) * int(custom_order_obj.custom_depth))
            if custom_order_obj.quantity > 20 or area > 20:
                total += (area * custom_order_obj.quantity)* custom_order_obj.custom_order.custom_price21   
            else:
                total += (area *  custom_order_obj.quantity)* custom_order_obj.custom_order.custom_price 
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
        print(":::::user_image:::::",user_image)
        print_name = self.request.session["form_1_data"]['print_name']
        context = {
            "custom_order_obj":custom_order_obj,
            "cart": cart,
            "date":date_,
            "total":total,
            "user_image": user_image,
            "print_name" : print_name,
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
            }  
        pdf = self.send_mail_PDF(template,context,user_mail)
        messages.success(self.request,"Order Received.\nYour Receipt is Sent to Your Email Address.")

    def get_form_step_data(self, form):
        data = super().get_form_step_data(form)
        if self.steps.step1 == 1:
            self.form1_data = self.request.session["form_1_data"] ={}
            self.form1_data["quantity"] = self.request.POST.getlist('quantity')
            self.form1_data["date_"] = self.request.POST.getlist('date_')
            self.form1_data["custom_order"] = self.request.POST
        return data

    def render(self, form=None, **kwargs):
        if self.steps.step1 == 4:
            if self.request.POST.get("2-accept") == "decline":
                self.storage.reset()
                self.request.session["form_1_data"] = ""
                return redirect("order-form")
        if self.steps.step1 > 1 and self.request.session["form_1_data"] == "":
            return redirect("order-form")
        return super(OrderForm, self).render(form, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(OrderForm, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 1:
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

        elif self.steps.step1 == 4:
            form1_data = self.request.session["form_1_data"]
            quantities = form1_data['quantity'] # list
            dates = form1_data['date_'] # list
            order = []
            for q,date in zip(quantities,dates):
                if q == "" or date == "":
                    continue
                qty = int(q.split("##")[0]) 
                pk = int(q.split("##")[1]) 
                product = get_object_or_404(ContainerPricing, id=pk)
                dictn = {
                    "product": product,
                    "qty":qty,
                    "date":date,
                }
                order.append(dictn)
            no_of_floors = form1_data["custom_order"]['no_of_floors']
            width = form1_data["custom_order"]['width']
            depth = form1_data["custom_order"]['depth']
            cus_qty = form1_data["custom_order"]['custom_quantity']
            cus_date = form1_data["custom_order"]['custom_date']
            custom_order = None
            if (no_of_floors != "" and width != "" and depth != "" and cus_qty !='' and cus_date != ""):
                qty = int(cus_qty.split("##")[0]) 
                pk = int(cus_qty.split("##")[1])      
                cus_product = get_object_or_404(CustomContainerPricing, id=pk)
                custom_order = {
                    "product":cus_product,
                    "qty": qty,
                    "date": cus_date,
                    "no_of_floors":no_of_floors,
                    "width":width,
                    "depth":depth,
                }
            context.update({
                "order":order,
                "custom_order":custom_order,
                })        
        return context 

    def done(self, form_list, **kwargs):
        forms = list(form_list)
        order_status = self.save_cart(forms[2])
        self.request.session["form_1_data"] = ""
        # print("done===",self.request.session.items())
        if order_status != "no order":
            buyer_form = forms[1]
            buyer_app = buyer_form.save(commit=False)
            buyer_app.user=self.request.user
            buyer_app.save()
            return redirect("/")
        else:
            messages.warning(self.request, "You must select something to place an order!")
            return redirect("order-form")


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
        area = (int(no_of_floors) * int(width) * int(depth))
        if qty > 20 or area > 20:
            total += (area * qty)* product.custom_price21  
        else:
            total += (area *  qty)* product.custom_price 
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