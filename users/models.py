from PIL import Image
from django.db import models
from datetime import datetime
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create Models

    
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



class SpecialUser(models.Model):

    USER_TYPE = (
        ('developer','Developer'),
        ('lender','Lender'),
        ('banker','Banker'),
    )
    
    is_active = models.BooleanField('Active', default=None)
    user_type = models.CharField('Sign up as', max_length=20, choices = USER_TYPE, default = None)
    f_name = models.CharField('First Name',max_length=100)
    l_name = models.CharField('Last Name',max_length=100)
    company_name = models.CharField('Name of Company',max_length=100)
    title = models.CharField('Title',max_length=100)
    email = models.EmailField('Email',max_length=100)
    phone_number = PhoneNumberField(("Phone Number"))
    activated_on = models.DateTimeField('Activated on()',blank=True, null=True)
    expire_time = models.DateTimeField('Expire On', blank=True, null=True)
    
    
    def __str__(self):
        return self.f_name

class SpecialUserLog(models.Model):
    specialuser = models.ForeignKey(SpecialUser, on_delete=models.CASCADE)
    userlog_datetime = models.DateTimeField('Logged in at (Datetime): ',blank=True, null=True)
    userlog_date = models.DateField('Logged in at: (Date)',blank=True, null=True)
    userlog_time = models.TimeField('Logged in at (Time): ',blank=True, null=True)




