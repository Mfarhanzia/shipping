from django.db import models
from multiselectfield import MultiSelectField
from localflavor.us.models import USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from users.models import User
# Create your models here.

class Order(models.Model):

    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    Type_Of_Development = (
        ('select all','Select All'),
        ('Commercial','Commercial'),
        ('Mixed-use','Mixed-use'),
        ('Multi-tenant','Multi-tenant'),
        ('Condominium','Condominium'),
        ('Townhome','Townhome'),
        ('Man Camp','Man Camp'),
        ('Mobile Home Park','Mobile Home Park'),
        ('RV Park','RV Park'),
        ('Park Home (as defined by Housing and Urban Development)','Park Home (as defined by Housing and Urban Development)'),
        ('Other','Other'),
    )

    Type_Of_Climate_Area = (

        ('select all','Select All'),
        ('Heavy Snow Load','Heavy Snow Load'),
        ('High Wind','High Wind'),
        ('Tornado','Tornado'),
        ('Earthquake','Earthquake'),
        ('Desert','Desert'),
        ('Other','Other '),
    )

    Type_Of_Smart_Home = (
    ('Automated Home Shopping and Delivery','Automated Home Shopping and Delivery'),
    ('Self-Driving Transport to Local Shopping Centers','Self-Driving Transport to Local Shopping Centers'),
    ('Self-Driving Transport to Local Medical Facilities','Self-Driving Transport to Local Medical Facilities'),
    )

    Type_Of_Electric_Vehicle_Function = (
        ('Standard','Standard'),
        ('Capability to Load Handicapped Person Without Human Assistance','Capability to Load Handicapped Person Without Human Assistance'),
    )

    company_name = models.CharField('Name of Company',max_length=100)
    f_name = models.CharField('First Name',max_length=100)
    l_name = models.CharField('Last Name',max_length=100)
    email = models.EmailField('Email',max_length=100)
    phone_number = PhoneNumberField(("Phone Number"), max_length = 18, help_text="XXX-XXX-XXXX")
    
    zipcode = USZipCodeField("Zip Code",blank=True, null=True)
    
    letter_of_credit = models.CharField("Do you have a Letter of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)

    how_much_letter_of_credit= models.CharField("What is the value of your Letter of Credit (in USD)?",max_length=50, help_text="in USD$", blank=True, null=True)
    # how_much_letter_of_credit= models.DecimalField("What is the value of your Letter of Credit (in USD)?", max_digits=20, decimal_places=2, help_text="in USD$", blank=True, null=True)

    line_of_credit = models.CharField("Do you have a Line of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)

    how_much_line_of_credit= models.CharField("What is the currently unused amount in your Line of Credit?",max_length=50, help_text="in USD$",blank=True, null=True)

    # how_much_line_of_credit= models.DecimalField("What is the currently unused       amount in your Line of Credit?",max_digits=20, decimal_places=2, help_text="in USD$", blank=True, null=True)
    STATUS_CHOICES = (("3-6 Months","3-6 Months"),
        ("6-9 Months", "6-9 Months"),
        ("1 Year or More", "1 Year or More"),
        )

    When_To_Order =(
        ('urgent','Urgent(within 30 days)'),
        ('other','Other'),
        )

    when_to_order = models.CharField("When are you looking to order?",choices=When_To_Order ,max_length=50, default=None)
    
    # other_when_to_order = models.PositiveIntegerField('Other (days)', validators=[MinValueValidator(31)], blank=True, null=True) 
    other_when_to_order = models.CharField("When To Order",choices=STATUS_CHOICES ,max_length=50, default=None, null=True, blank=True)

    type_of_development = MultiSelectField("What type of development(s) are you seeking?",choices=Type_Of_Development, max_length=300, blank=True, null=True)

    other_type_of_development = models.CharField(max_length=300, verbose_name="Other", null=True, blank=True)
   
    type_of_climate_area = MultiSelectField("On which type of climate area(s) will the development(s) be sited? ",choices=Type_Of_Climate_Area, max_length=300, blank=True, null=True)
    
    other_type_of_climate_area =models.CharField(max_length=200, verbose_name="Other", null=True, blank=True)
   

    type_of_smart_home = MultiSelectField("What type of smart home functionality are you interested in learning more about? ",choices=Type_Of_Smart_Home, max_length=300, blank=True, null=True)
   
    type_of_electric_vehicle_function = MultiSelectField("An electric vehicle will be included with each housing unit. What type of electric vehicle function are you interested in?",choices=Type_Of_Electric_Vehicle_Function, max_length=300, blank=True, null=True)

    learn_about_electric_drive = models.CharField("Do you wish to learn more about an optional electric-drive community transport vehicle?",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True)

    septic_infrastructure  = models.CharField("Does the development site already have septic infrastructure or service?",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True)

    installation_septic_infrastructure  = models.CharField("Does it require the installation of septic infrastructure? (There will be a charge for initial infrastructure installation and periodic maintenance service charges.) ",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True, default=None)


    # class Meta:
    #     ordering = ('-when_to_order', '-how_much_letter_of_credit', '-how_much_line_of_credit') 


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

    class Meta:
        verbose_name = "Containers Pricing"
        verbose_name_plural = "Containers Pricing"

    def __str__(self):
        return f"{self.no_of_floors} {self.variant}"


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order_items = models.ForeignKey(ContainerPricing, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField("Quantity")
    ordered_on = models.DateTimeField(auto_now_add=True)
