from PIL import Image
from django.db import models
from datetime import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create Models

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    username = models.CharField(verbose_name='Username',max_length=255,default=None, blank=True, null= True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_dealer(self):
        try:
            self.dealer
            return True
        except:
            return False


class SpecUser(User):
    USER_TYPE = (
        ('developer','Developer'),
        ('lender','Lender'),
        ('banker','Banker'),
        ('dealer','Dealer'),
        ('homeowner','Prospective Homeowner'),
        ('Municipality/Government Official','Municipality/Government Official'),
        ('vendor','Vendor'),
    )

    user_type = models.CharField('Sign up as', max_length=32, choices = USER_TYPE, default = None)
    company_name = models.CharField('Name of Company',max_length=100, blank=True, null=True)
    title = models.CharField('Title',max_length=100, blank=True, null=True)
    phone_number = models.CharField(("Phone Number"), max_length = 18, help_text="optional", blank=True, null=True)
    dealer_no = models.CharField('Dealer Number',max_length=6, help_text="optional", validators=[RegexValidator(r"^[0-9]*$")] ,blank=True, null=True)
    home_permission = models.BooleanField('Home Access', default=False)
    content_permission = models.BooleanField('Content Access', default=False)
    activation_time_home = models.DateTimeField('Activation Time (Home)',blank=True, null=True)
    expire_time_home = models.DateTimeField('Expire Time (Home)', blank=True, null=True) 
    activation_time_spec_content = models.DateTimeField('Activation Time (Content)',blank=True, null=True)
    expire_time_spec_content = models.DateTimeField('Expire Time (Content)', blank=True, null=True) 

    city = models.CharField('City',max_length=60, default='', blank=True, null=True)
    postal = models.CharField('Postal',max_length=60, default='', blank=True, null=True)
    state = models.CharField('State',max_length=60, default='', blank=True, null=True)
    country = models.CharField('Country',max_length=60, default='', blank=True, null=True)
    address = models.CharField('Address', max_length=1000, default='', blank=True, null=True)

    def __str__(self):
        return f"{self.user_type} - {self.first_name}"

    class Meta:
        verbose_name = 'Spec_User'
        verbose_name_plural = 'Spec User'


class EmailList(models.Model):
    # name = models.CharField("Name", max_length=60, blank=True, null=True, default=None)
    email = models.EmailField(("Email"), max_length=254, unique=True)


class UserPreferences(models.Model):
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
   
    Type_Of_Smart_Home = (
    ('Automated Home Shopping and Delivery','Automated Home Shopping and Delivery'),
    ('Self-Driving Transport to Local Shopping Centers','Self-Driving Transport to Local Shopping Centers'),
    ('Self-Driving Transport to Local Medical Facilities','Self-Driving Transport to Local Medical Facilities'),
    )
    Type_Of_Electric_Vehicle_Function = (
        ('Standard','Standard'),
        ('Capability to Load Handicapped Person Without Human Assistance','Capability to Load Handicapped Person Without Human Assistance'),
    )

    user_obj = models.ForeignKey(SpecUser, on_delete=models.CASCADE)
    type_of_development = MultiSelectField("What type of development(s) are you seeking?",choices=Type_Of_Development, max_length=300)

    other_type_of_development = models.CharField(max_length=300, verbose_name="Other", blank=True, null=True)
   
    type_of_smart_home = MultiSelectField("What type of smart home functionality are you interested in learning more about? ",choices=Type_Of_Smart_Home, max_length=300)
   
    type_of_electric_vehicle_function = MultiSelectField("An electric vehicle will be included with each housing unit. What type of electric vehicle function are you interested in?",choices=Type_Of_Electric_Vehicle_Function, max_length=300)

    learn_about_electric_drive = models.CharField("Do you wish to learn more about an optional electric-drive community transport vehicle?",choices=YES_NO_CHOICES, max_length=100)

    class Meta:
        verbose_name = 'UserPreference'
        verbose_name_plural = 'UserPreferences'


class ModelsInfo(models.Model):
    model_name = models.CharField('Model name',max_length=60, default='', blank=True, null=True)
    model_dimension = models.CharField('Model Dimensions',max_length=60, default='', blank=True, null=True)
    model_header = models.CharField('Model Header',max_length=60, default='', blank=True, null=True)
    model_text = models.TextField('Text', default='', blank=True, null=True)
    beds = models.CharField('Beds',max_length=60, default='', blank=True, null=True)
    baths = models.CharField('Baths',max_length=60, default='', blank=True, null=True)
    sq_ft = models.CharField('SQ.ft',max_length=60, default='', blank=True, null=True)
    parking_spaces = models.CharField('Parking Spaces',max_length=60, default='', blank=True, null=True)
    no_of_kitchen = models.CharField('Number of Kitchen',max_length=60, default='', blank=True, null=True)
    kitchen = models.CharField('Kitchen',max_length=60, default='', blank=True, null=True)
    bathroom = models.CharField('Bathroom',max_length=60, default='', blank=True, null=True)
    frame_material = models.CharField('Frame Material',max_length=60, default='', blank=True, null=True)
    price = models.CharField('Price',max_length=60, default='', blank=True, null=True)
    amenities = models.CharField('Amenities',max_length=60, default='', blank=True, null=True)
    floor = models.CharField('floor',max_length=60, default='', blank=True, null=True)
    garage = models.CharField('Garage',max_length=60, default='', blank=True, null=True)
    fireplace = models.CharField('Fireplace',max_length=60, default='', blank=True, null=True)
    laundry = models.CharField('Laundry',max_length=60, default='', blank=True, null=True)
    interior_features = models.CharField('Interior Features',max_length=60, default='', blank=True, null=True)
    construction_material = models.CharField('Construction Materials',max_length=60, default='', blank=True, null=True)


class ModelImages(models.Model):
    modelsinfo_obj = models.ForeignKey(ModelsInfo, on_delete=models.CASCADE)
    path = models.CharField('Beds',max_length=900, default='', blank=True, null=True)



