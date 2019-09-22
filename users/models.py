from PIL import Image
from django.db import models
from datetime import datetime
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    )

    user_type = models.CharField('Sign up as', max_length=32, choices = USER_TYPE, default = None)
    company_name = models.CharField('Name of Company',max_length=100, blank=True, null=True)
    title = models.CharField('Title',max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(("Phone Number"), max_length = 18, help_text="XXX-XXX-XXXX")
    dealer_no = models.CharField('Dealer Number',max_length=6, validators=[RegexValidator(r"^[0-9]*$")] ,blank=True, null=True)

    home_permission = models.BooleanField('Home Access', default=None)
    content_permission = models.BooleanField('Content Access', default=None)
    activation_time_home = models.DateTimeField('Activation Time (Home)',blank=True, null=True)
    expire_time_home = models.DateTimeField('Expire Time (Home)', blank=True, null=True) 
    activation_time_spec_content = models.DateTimeField('Activation Time (Content)',blank=True, null=True)
    expire_time_spec_content = models.DateTimeField('Expire Time (Content)', blank=True, null=True) 
    
    def __str__(self):
        return f"{self.user_type} {self.first_name}"


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
    email = models.EmailField(("Email"), max_length=254, unique = True)