from django.db import models
from multiselectfield import MultiSelectField
from localflavor.us.models import USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from users.models import User

# Create your models here.

class Order(models.Model):
    Type_Of_Climate_Area = (
        ('select all','Select All'),
        ('Heavy Snow Load','Heavy Snow Load'),
        ('High Wind','High Wind'),
        ('Tornado','Tornado'),
        ('Earthquake','Earthquake'),
        ('Desert','Desert'),
        ('Other','Other '),
    )
    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    f_name = models.CharField('First Name',max_length=100)
    l_name = models.CharField('Last Name',max_length=100)
    email = models.EmailField('Email',max_length=100, help_text="Optional", blank=True, null=True)
    company_name = models.CharField('Name of Company',max_length=100, help_text="Optional", blank=True, null=True)
    # phone_number = PhoneNumberField(("Phone Number"), max_length = 18, help_text="Optional", blank=True, null=True)
    phone_number = models.CharField(("Phone Number"), max_length = 18, help_text="Optional", blank=True, null=True)
  
    zipcode = USZipCodeField("Zip Code",blank=True, null=True)
    
    letter_of_credit = models.CharField("Do you have a Letter of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)
    how_much_letter_of_credit= models.CharField("What is the value of your Letter of Credit (in USD)?",max_length=50, help_text="in USD$", blank=True, null=True)

    line_of_credit = models.CharField("Do you have a Line of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)
    how_much_line_of_credit= models.CharField("What is the currently unused amount in your Line of Credit?",max_length=50, help_text="in USD$",blank=True, null=True)

    STATUS_CHOICES = (("3-6 Months","3-6 Months"),
        ("6-9 Months", "6-9 Months"),
        ("1 Year or More", "1 Year or More"),
        )

    When_To_Order =(
        ('urgent','Urgent(within 30 days)'),
        ('other','Other'),
        )
    when_to_order = models.CharField("When are you looking to order?",choices=When_To_Order ,max_length=50, default=None, null=True, blank=True)
    other_when_to_order = models.CharField("When To Order",choices=STATUS_CHOICES ,max_length=50, default=None, null=True, blank=True)
    
    type_of_climate_area = MultiSelectField("On which type of climate area(s) will the development(s) be sited? ",choices=Type_Of_Climate_Area, max_length=300, blank=True, null=True)
    other_type_of_climate_area =models.CharField(max_length=200, verbose_name="Other", null=True, blank=True)

    septic_infrastructure  = models.CharField("Does the development site already have septic infrastructure or service?",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True)

    installation_septic_infrastructure  = models.CharField("Does it require the installation of septic infrastructure? (There will be a charge for initial infrastructure installation and periodic maintenance service charges.) ",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Buyer Application"
        verbose_name_plural = "Buyer Applications"


class Material(models.Model):
    """Material Required showing this data to vendors for quotations"""
    name = models.CharField("Material Name", max_length=100)


class MaterialQuotations(models.Model):
    material_name = models.CharField("Material Name", max_length=100,default=None)
    user_name = models.CharField("Name:", max_length=100)
    company_name = models.CharField("Company Name:", max_length=100)
    price = models.CharField("Price", max_length=100)
    time_date = models.DateTimeField("Quotation Date", auto_now_add=True)

    class Meta:
        verbose_name = "MaterialQuotation"
        verbose_name_plural = "MaterialQuotations"


class ContainerPricing(models.Model):
    no_of_floors = models.CharField("No. of Floors", max_length=100)
    variant = models.CharField("Variant", max_length=100)
    square_feet = models.CharField("Approximate Square Feet", max_length=100)
    price = models.DecimalField("Price", max_digits=20, decimal_places=2)
    price21 = models.DecimalField("Delivered Price Delivered to site for 21 or more units", max_digits=20, decimal_places=2, blank=True, null=True)
    model_image = models.CharField("Model Image", max_length=1000, blank=True, null=True)
    model_name = models.CharField("Model Name", max_length=100, blank=True, null=True, default='')
    model_link = models.CharField("model_link", max_length=10, blank=True, null=True, default='')
    class Meta:
        verbose_name = "Containers Pricing"
        verbose_name_plural = "Containers Pricing"

    def __str__(self):
        return f"{self.no_of_floors} {self.variant}"


class CustomContainerPricing(models.Model):
    sqfeet_per_room = models.CharField("Approximate Square Feet per room", max_length=100)
    custom_price = models.DecimalField("Price per 290s.f. room(for 20units or less)", max_digits=20, decimal_places=2)
    custom_price21 = models.DecimalField("Price per 290s.f. room(for 21units or more)", max_digits=20, decimal_places=2, blank=True, null=True) 
    class Meta:
        verbose_name = "Custom Containers Pricing"
        verbose_name_plural = "Custom  Containers Pricing"

    def __str__(self):
        return f"Custom Container Pricing"


class DeliveryInfo(models.Model):
    address = models.CharField('Address', max_length=1000, default='')
    city = models.CharField('City',max_length=60, default='')
    state = models.CharField('State',max_length=60, default='')
    postal = USZipCodeField('Postal',max_length=60, default='')
    country = models.CharField('Country',max_length=60, default='')
    delivery_date = models.DateField(default=None)

    class Meta:
        verbose_name = "Delivery Info"
        verbose_name_plural = "Delivery Info"


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_info_obj = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    buyer_app_obj = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, blank=True, null=True)
    order_items = models.ForeignKey(ContainerPricing, on_delete=models.CASCADE, blank=True, null=True)
    custom_order = models.ForeignKey(CustomContainerPricing, on_delete=models.CASCADE, blank=True, null=True)
    custom_floors = models.CharField("No. of Floors", max_length=100, blank=True, null=True)
    custom_width = models.CharField("Width", max_length=100, blank=True, null=True)
    custom_depth = models.CharField("Depth", max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField("Quantity")
    ordered_on = models.DateField(auto_now_add=True)
    furnishing_option = models.CharField('furnishing_option', max_length=100, blank=True, null=True)
    user_image = models.ImageField(upload_to="pdf-images", blank=True, null=True, default="default.jpeg")

    class Meta:
        verbose_name = "Shipping Home Order"
        verbose_name_plural = "Shipping Home Orders"
