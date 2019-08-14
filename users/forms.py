import re
from django import forms
from .models import SpecialUser, EmailList, User
from phonenumber_field.modelfields import PhoneNumberField
class SpecialUserForm(forms.ModelForm):
    class Meta:
        model = SpecialUser

        fields = ('user_type','f_name','l_name','company_name','title','email','dealer_no','phone_number')

        widgets = {
            'user_type': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        
        super(SpecialUserForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({
            'id': 'id_phone_number_8'
        })

    def clean_f_name(self):
        f_name = self.cleaned_data.get("f_name")
        f = re.findall("^[a-zA-Z]+$", f_name)
        if not f:
            raise forms.ValidationError(
                'Incorrect First Name')
        return f_name

    def clean_l_name(self):
        l_name = self.cleaned_data.get("l_name")
        l =re.findall("^[a-zA-Z]+$", l_name)
        if not l:
            raise forms.ValidationError(
                'Incorrect Last Name')
        return l_name
    def clean_email(self):
        email = self.cleaned_data['email']
        if self.cleaned_data['user_type'] == 'dealer':
            if User.objects.filter(email=email):
                raise forms.ValidationError(
                    'Already Exist'
                )
        return email
    
class EmailListForm(forms.ModelForm):

    class Meta:
        model = EmailList
        fields = ('email',)