import re
from django import forms
from .models import SpecialUser, EmailList

class SpecialUserForm(forms.ModelForm):
    class Meta:
        model = SpecialUser

        fields = ('user_type','f_name','l_name','company_name','title','email','dealer_no','phone_number',)

        widgets = {
            'user_type': forms.RadioSelect(),
        }

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

class EmailListForm(forms.ModelForm):

    class Meta:
        model = EmailList
        fields = ('email',)