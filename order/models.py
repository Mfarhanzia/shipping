from django.db import models
from multiselectfield import MultiSelectField
from localflavor.us.models import USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator

# Create your models here.

class Order(models.Model):

    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    Type_Of_Development = (
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
    phone_number = PhoneNumberField(("Phone Number"))
    
    zipcode = USZipCodeField("Zip Code",blank=True, null=True)
    
    letter_of_credit = models.CharField("Do you have a Letter of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)
    how_much_letter_of_credit= models.PositiveIntegerField("What is the value of your Letter of Credit (in USD)?", blank=True, null=True)
    
    line_of_credit = models.CharField("Do you have a Line of Credit?", max_length=5, choices= YES_NO_CHOICES, blank=True, null=True)
    how_much_line_of_credit= models.PositiveIntegerField("What is the currently unused amount in your Line of Credit?", blank=True, null=True)

    When_To_Order =(
        ('urgent','Urgent(within 30 days)'),
        ('other','Other (days)'),
        )

    when_to_order = models.CharField("When are you looking to order?",choices=When_To_Order ,max_length=50, default=None)
    
    other_when_to_order = models.PositiveIntegerField('Other (days)', validators=[MinValueValidator(31)], blank=True, null=True) 

    type_of_development = MultiSelectField("What type of development(s) are you seeking?",choices=Type_Of_Development, max_length=300, blank=True, null=True)

    other_type_of_development =models.CharField(max_length=300, verbose_name="Other", null=True, blank=True)
   
    type_of_climate_area = MultiSelectField("On which type of climate area(s) will the development(s) be sited? ",choices=Type_Of_Climate_Area, max_length=300, blank=True, null=True)
    
    other_type_of_climate_area =models.CharField(max_length=200, verbose_name="Other", null=True, blank=True)
   

    type_of_smart_home = MultiSelectField("What type of smart home functionality are you interested in learning more about? ",choices=Type_Of_Smart_Home, max_length=300, blank=True, null=True)
   
    type_of_electric_vehicle_function = MultiSelectField("An electric vehicle will be included with each housing unit. What type of electric vehicle function are you interested in?",choices=Type_Of_Electric_Vehicle_Function, max_length=300, blank=True, null=True)

    learn_about_electric_drive = models.CharField("Do you wish to learn more about an optional electric-drive community transport vehicle?",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True)

    septic_infrastructure  = models.CharField("Does the development site already have septic infrastructure or service?",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True)

    installation_septic_infrastructure  = models.CharField("Does it require the installation of septic infrastructure? (There will be a charge for initial infrastructure installation and periodic maintenance service charges.) ",choices=YES_NO_CHOICES, max_length=100, blank=True, null=True, default=None)


    class Meta:
        ordering = ('-when_to_order','-how_much_line_of_credit') 