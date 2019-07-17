from django import forms
from .models import SpecialUser

class SpecialUserForm(forms.ModelForm):

    class Meta:
        model = SpecialUser

        fields = ('user_type','f_name','l_name','company_name','title','email','phone_number',)

        widgets = {
            'user_type': forms.RadioSelect(),
        }