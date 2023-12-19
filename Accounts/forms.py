from django import forms
import re
from django.core.exceptions import ValidationError,FieldError
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from .models import Registration
from .models import UserProfile

class Registrationform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))
    class Meta:
        model=Registration
        fields= ['firstname','lastname','email','password','confirmpassword']

    def __init__(self,*args,**kwargs):
        super(Registrationform,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    

    def clean_username(self, name, field_name):
        # Check if the username contains only alphabets
        if not re.match("^[a-zA-Z]+$", name):
            raise forms.ValidationError(f"{field_name} should only contain alphabets.")
        return name

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check for minimum length and common passwords
        validators = [
            MinimumLengthValidator(),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]

        errors = []

        for validator in validators:
            try:
                validator.validate(password)
            except ValidationError as e:
                errors.extend(e.error_list)

        # Check for the inclusion of special characters, lowercase letters, and uppercase letters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(ValidationError("Password must contain at least one special character."))

        if not re.search(r'[a-z]', password):
            errors.append(ValidationError("Password must contain at least one lowercase letter."))

        if not re.search(r'[A-Z]', password):
            errors.append(ValidationError("Password must contain at least one uppercase letter."))

        # Your custom password validation goes here
        # For example, you might want to ensure it doesn't contain the username or other specific rules

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
     cleaned_data = super(Registrationform, self).clean()
     password = cleaned_data.get('password')
     confirm_password = cleaned_data.get('confirmpassword')

     if password and confirm_password and password != confirm_password:
        raise forms.ValidationError('Password does not match.')

     cleaned_data['firstname'] = self.clean_username(cleaned_data.get('firstname'), 'FirstName')
     cleaned_data['lastname'] = self.clean_username(cleaned_data.get('lastname'), 'LastName')

     return cleaned_data
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("firstname", "lastname")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields["firstname"].widget.attrs["placeholder"] = "First Name"
        self.fields["lastname"].widget.attrs["placeholder"] = "Last Name"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control bg-dark text-white"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"



class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={"invalid": ("Image Files Only")},
        widget=forms.FileInput,
    )

    class Meta:
        model = UserProfile
        fields = (
            "address",
            "phone_number",
            "city",
            "state",
            "country",
            "profile_picture",
        )

