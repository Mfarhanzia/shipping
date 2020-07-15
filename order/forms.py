import re
from django import forms
from .models import Order, MaterialQuotations, DeliveryInfo
from django.contrib.auth import password_validation, authenticate


class BuyerAppForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('type_of_climate_area','other_type_of_climate_area', 'septic_infrastructure','installation_septic_infrastructure')

        widgets = {
            'septic_infrastructure' : forms.RadioSelect(),
            'installation_septic_infrastructure' : forms.RadioSelect(),    
            }
    field_order = ('type_of_climate_area','other_type_of_climate_area', 'septic_infrastructure','installation_septic_infrastructure')


class BuyerAppForm2(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('f_name', 'l_name', 'email', 'company_name', 'phone_number', 'letter_of_credit',
                  'how_much_letter_of_credit','line_of_credit','how_much_line_of_credit')

        widgets = {
            # 'when_to_order' : forms.RadioSelect(),
            'letter_of_credit' : forms.RadioSelect(),
            'line_of_credit' : forms.RadioSelect(),
        }

    field_order = ('f_name','l_name','email', 'company_name', 'phone_number','letter_of_credit',
                   'how_much_letter_of_credit','line_of_credit','how_much_line_of_credit')

    # def __init__(self, *args, **kwargs):
    #     super(BuyerAppForm2, self).__init__(*args, **kwargs)
    #     self.fields['other_when_to_order'].widget.attrs.update({
    #         'class': 'form-control'
    #     })

    def clean_f_name(self):
        f_name = self.cleaned_data.get("f_name")
        f = re.findall("^[a-zA-Z]+$", f_name)
        if not f:
            raise forms.ValidationError('Incorrect First Name')
        return f_name

    def clean_l_name(self):
        l_name = self.cleaned_data.get("l_name")
        l =re.findall("^[a-zA-Z]+$", l_name)
        if not l:
            raise forms.ValidationError('Incorrect Last Name')
        return l_name

    def clean_how_much_letter_of_credit(self):
        if not self.cleaned_data.get("how_much_letter_of_credit"):
            letter_of_credit = self.cleaned_data.get("how_much_letter_of_credit")
            letter_of_credit = '0'
            return letter_of_credit
        else:
            try:
                letter_of_credit = self.cleaned_data.get("how_much_letter_of_credit").replace('$','').replace(',','')
                return letter_of_credit
            except:
                pass
    #        # return letter_of_credit

    def clean_how_much_line_of_credit(self):
        if not self.cleaned_data.get("how_much_line_of_credit"):
            line_of_credit = self.cleaned_data.get("how_much_line_of_credit")
            line_of_credit = '0'
            return line_of_credit

        else:
            try:
                line_of_credit = self.cleaned_data.get("how_much_line_of_credit").replace('$','').replace(',','')

                return line_of_credit
            except:
                pass
    #         # return line_of_credit


class DeliveryInfoForm(forms.ModelForm):
    delivery_date = forms.DateField(required=True, label='Date Delivered to site', widget=forms.TextInput(attrs={"type":"date"}), )

    class Meta:
        model = DeliveryInfo
        exclude = ('order_obj',)



class MaterialQuotationsForm(forms.ModelForm):
    class Meta:
        model = MaterialQuotations
        fields = ("price",)


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 200)]
OTHER_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 50)]
FLOOR_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 13)]
# print(PRODUCT_QUANTITY_CHOICES.a)
PRODUCT_QUANTITY_CHOICES[0]=("","-")
FLOOR_QUANTITY_CHOICES[0]=("","-")
OTHER_QUANTITY_CHOICES[0]=("","-")

    
class AddCustomProductForm(forms.Form):
    no_of_floors = forms.ChoiceField(choices=FLOOR_QUANTITY_CHOICES, required=False)
    width = forms.ChoiceField(choices=OTHER_QUANTITY_CHOICES, required=False)
    depth = forms.ChoiceField(choices=OTHER_QUANTITY_CHOICES, required=False)

class UserTermsForm(forms.Form):
    CHOICES = (
        ("decline","Decline"),
        ("agree","Agree"),
    )
    accept = forms.ChoiceField(label="",choices=CHOICES, widget=forms.RadioSelect)
    image_field = forms.CharField(label="",widget=forms.TextInput(attrs={"id":"image-input_id", "type":"hidden"}), required=False)
    print_name = forms.CharField(label="Signature",widget=forms.TextInput(attrs={"id":"print_name","class":" pl-1"}))


class LoginForm(forms.Form):
    # this form is only used in formwizard login
    email = forms.CharField(label="Email", required=True)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(render_value=True,),
    )

    def clean(self):
        print("running clean email")
        form_data = self.cleaned_data
        email = form_data.get("email")
        password = form_data.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError(
                'Incorrect Email or Password',
                code='password_mismatch',
            )
        return email

