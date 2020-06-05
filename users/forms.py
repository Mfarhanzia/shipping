import re
from django import forms
from .models import EmailList, User, SpecUser, UserPreferences
from django.contrib.auth import password_validation
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
   
   
class EmailListForm(forms.ModelForm):

    class Meta:
        model = EmailList
        fields = ['email']
    def __init__(self, *args, **kwargs):
        super(EmailListForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'email@email.com',
            "class":"news-input",
        })


class SpecUserForm(forms.ModelForm):
    pass


class RegistrationForm1(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(render_value=True,),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(render_value=True,),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        model = SpecUser
        fields = ('first_name','last_name', 'email','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password Mismatch',
                code='password_mismatch',
            )
        return password2

    def clean_first_name(self):
        f_name = self.cleaned_data.get("first_name")
        f = re.findall("^[a-zA-Z]+$", f_name)
        if not f:
            raise forms.ValidationError('Incorrect First Name')
        return f_name

    def clean_last_name(self):
        l_name = self.cleaned_data.get("last_name")
        l =re.findall("^[a-zA-Z]+$", l_name)
        if not l:
            raise forms.ValidationError(
                'Incorrect Last Name'
                )
        return l_name
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)


class RegistrationForm2(forms.ModelForm):
    class Meta:
        model = SpecUser
        fields = ('user_type', 'company_name','title','dealer_no','phone_number')
        # widgets = {
        #     'user_type': forms.RadioSelect(),
        # }




class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ("type_of_development","other_type_of_development","type_of_smart_home","type_of_electric_vehicle_function","learn_about_electric_drive",)

        widgets = {
            'learn_about_electric_drive' : forms.RadioSelect(),}

    # def __init__(self, *args, **kwargs):
    #     super(UserPreferencesForm, self).__init__(*args, **kwargs)
    #     self.fields['type_of_development'].widget.attrs.update({
    #         "class":"checkbox-container",})
    #     self.fields['type_of_smart_home'].widget.attrs.update({
    #         "class":"",})
    #     self.fields['type_of_electric_vehicle_function'].widget.attrs.update({
    #         "class": "", })
    #     self.fields['learn_about_electric_drive'].widget.attrs.update({

    #         "class":"",})


class ContactUsForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message','class':"p-1", "rows":"4"}), required=True)