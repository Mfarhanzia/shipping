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
    phone_number = PhoneNumberField(("Phone Number"), max_length = 18, help_text="Optional", blank=True, null=True)
    dealer_no = models.CharField('Dealer Number',max_length=6, validators=[RegexValidator(r"^[0-9]*$")] ,blank=True, null=True)

    home_permission = models.BooleanField('Home Access', default=False)
    content_permission = models.BooleanField('Content Access', default=False)
    activation_time_home = models.DateTimeField('Activation Time (Home)',blank=True, null=True)
    expire_time_home = models.DateTimeField('Expire Time (Home)', blank=True, null=True) 
    activation_time_spec_content = models.DateTimeField('Activation Time (Content)',blank=True, null=True)
    expire_time_spec_content = models.DateTimeField('Expire Time (Content)', blank=True, null=True) 
    
    def __str__(self):
        return f"{self.user_type} - {self.first_name}"

    class Meta:
        verbose_name = 'Spec_User'
        verbose_name_plural = 'Spec User'


class Photo(models.Model):
    original_image = models.ImageField(upload_to='photos' , default=None)
    watermarked_image = models.ImageField(upload_to='wartermarked_photos', default=None, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.original_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (640, 500)
            img.thumbnail(output_size)
            img.save(self.original_image.path)  


class WaterMark(models.Model):
    water_mark_image = models.ImageField(upload_to='water_mark', default=None, help_text="You can add atmost one WaterMark image")
    
    @staticmethod
    def __str__():
        return f'Water Marker'


class EmailList(models.Model):
    name = models.CharField("Name", max_length=60, blank=True, null=True)
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