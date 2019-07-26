import re
from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order

        fields = ('company_name','f_name','l_name','email','phone_number','zipcode','letter_of_credit','how_much_letter_of_credit','line_of_credit','how_much_line_of_credit','when_to_order', 'other_when_to_order','type_of_development','other_type_of_development','type_of_climate_area','other_type_of_climate_area','type_of_smart_home','type_of_electric_vehicle_function','learn_about_electric_drive','septic_infrastructure','installation_septic_infrastructure')
    

        widgets = {
            'when_to_order' : forms.RadioSelect(),
            'letter_of_credit' : forms.RadioSelect(),
            # 'how_much_letter_of_credit' : forms.CharField(attrs={'autocomplete':'off'}),
            'line_of_credit' : forms.RadioSelect(),
            'learn_about_electric_drive' : forms.RadioSelect(),
            'septic_infrastructure' : forms.RadioSelect(),
            'installation_septic_infrastructure' : forms.RadioSelect(),    
        }
    def __init__(self, *args, **kwargs):
        print('+++++++++++++++=')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['how_much_letter_of_credit'].widget.attrs.update({
            'autocomplete': 'off'
        })



    def clean_f_name(self):
        
        f_name = self.cleaned_data.get("f_name")
       
        f = re.findall("^[a-zA-Z]+$", f_name)
        if not f:
            raise forms.ValidationError(
                'Incorrect First Name'
                )
        return f_name

    def clean_l_name(self):
        l_name = self.cleaned_data.get("l_name")
        l =re.findall("^[a-zA-Z]+$", l_name)
        if not l:
            raise forms.ValidationError(
                'Incorrect Last Name'
                )
        return l_name     