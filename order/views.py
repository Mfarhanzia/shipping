
import random
import string
from .import utils
from PIL import Image
from .models import Order
from .forms import OrderForm
from datetime import datetime
from django.db.models import F
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.utils.encoding import force_text
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from users .models import SpecialUser, SpecialUserLog, Photo, WaterMark
from django.db.models import FloatField
from django.db.models.functions import Cast
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

        message = render_to_string('order/order_mail_to_admin.html', {
            'form': form.cleaned_data, })
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
        mail_subject = f"Order Confirmation"
        message = render_to_string('order/order_confirm_mail.html', {
            'form': form, })
        to_email = form['email']
        email = EmailMessage(subject=mail_subject,body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email], bcc=("farhan71727@gmail.com",))
        email.content_subtype = "html"
        email.send()

class ViewOrder(LoginRequiredMixin,ListView):
    """
    view for showing orders for authenticated users
    """
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
        # qs = Order.objects.order_by('-when_to_order','-how_much_letter_of_credit','-how_much_line_of_credit')
        
        qs = Order.objects.annotate(fieldsum=(Cast('how_much_letter_of_credit',FloatField())) + (Cast('how_much_line_of_credit',FloatField()))).order_by('-when_to_order', '-fieldsum')
        
        for i in qs:
            print(type(i.fieldsum),i.fieldsum)
        return qs

# custom decorator
def give_special_access(func):
    def wrapper(request, *args,**kwargs):
        """
        decorator checks the user expire time with current time.
        checks if time
        """
        uid = utils.decrypt(kwargs['uidb64']) # decrypt the userid from url

        user = get_object_or_404(SpecialUser, is_active=True, pk=uid)

        if user and user.expire_time and timezone.now() < user.expire_time: 
            
            time1 = user.expire_time - timezone.now()
            time = user.expire_time.timestamp() - timezone.now().timestamp()
            return func(request, time,*args,**kwargs)
        else:
            user.expire_time = None
            user.activated_on = None
            user.save()
            messages.warning(request, f'Link is Expired!')
            return redirect('/')
    return wrapper

def check_session(func):
  
    def wrapper(request,*args, **kwargs):
        """
        This function checks if the user opens this page first time it makes a session name "logkey" asign a random string to it and adds the current time as login time else if the "logkey" session alredy has value that means user is logged in and it will not save the current time as log in time. 
        """
        uid = utils.decrypt(kwargs['uidb64'])
   
        if uid not in request.session.keys():
            request.session[uid] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            #entering login time
            # uid = utils.decrypt(kwargs['uidb64'])
            user = get_object_or_404(SpecialUser, is_active=True, pk=uid)
            SpecialUserLog.objects.create(specialuser=user, userlog_datetime=timezone.now(), userlog_date=timezone.now(), userlog_time=timezone.now())
            return func(request, *args,**kwargs)
        else:
            return func(request, *args,**kwargs)

    return wrapper
        

def watermark_photo(input_image_path,
                    output_image_path,
                    watermark_image_path,id):
    """
    Adding watermark and saving in Photo.watermarked_image field

    """
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path).convert("RGBA")
    
    watermark.putalpha(150)

    width, height = base_image.size
    
    # pixdata = watermark.load()
    # watermark_width, watermark_height = watermark.size

    # for y in range(watermark_height):
    #     for x in range(watermark_width):
    #         if pixdata[x, y] == (255, 255, 255, 255):
    #             pixdata[x, y] = (255, 255, 255, 100)

    
    width_of_watermark , height_of_watermark = watermark.size
    position1 = (int(width/2-width_of_watermark/2),int(height/2-height_of_watermark/2))
    
    transparent = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, position1, mask=watermark)
    transparent.save(output_image_path)

    # return transparent
    a = Photo.objects.get(id=id)
    path = output_image_path.split('/',1)
    
    a.watermarked_image = path[1]
    a.save()
    
@give_special_access
@check_session
def specialuser_ViewOrder(request,time,uidb64):
    """
    This view is for Special user to whom access given by admin for 12 hrs
    """
    image = Photo.objects.all()
    water_mark = WaterMark.objects.first()    
    if water_mark:
        for img in image:
            id=img.id
            if not img.watermarked_image:
                watermark_photo(img.original_image,'media/wartermarked_photos/water_marked'+str(id)+'.png', water_mark.water_mark_image, id = id)

    image = Photo.objects.all()
    # qs = Order.objects.order_by('-when_to_order', '-how_much_letter_of_credit','-how_much_line_of_credit')
    
    qs = Order.objects.annotate(fieldsum=(Cast('how_much_letter_of_credit',FloatField())) + (Cast('how_much_line_of_credit',FloatField()))).order_by('-when_to_order', '-fieldsum')
    return render(request, 'order/view_orders.html', {'orders':qs,'time':int(time),'uid': uidb64, 'image':image, 'title': 'Orders' })
    