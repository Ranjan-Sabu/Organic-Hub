from django import forms
import re
from django.core.exceptions import ValidationError, FieldError
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from .models import Registration
from .models import UserProfile


class Registrationform(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Password", "class": "form-control"}
        )
    )
    confirmpassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        )
    )

    class Meta:
        model = Registration
        fields = ["firstname", "lastname", "email", "password", "confirmpassword"]

    def __init__(self, *args, **kwargs):
        super(Registrationform, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean_username(self, name, field_name):
        # Check if the username contains only alphabets
        if not re.match("^[a-zA-Z]+$", name):
            raise forms.ValidationError(f"{field_name} should only contain alphabets.")
        return name

    def clean_password(self):
        password = self.cleaned_data.get("password")

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
            errors.append(
                ValidationError("Password must contain at least one special character.")
            )

        if not re.search(r"[a-z]", password):
            errors.append(
                ValidationError("Password must contain at least one lowercase letter.")
            )

        if not re.search(r"[A-Z]", password):
            errors.append(
                ValidationError("Password must contain at least one uppercase letter.")
            )

        # Your custom password validation goes here
        # For example, you might want to ensure it doesn't contain the username or other specific rules

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super(Registrationform, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirmpassword")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match.")

        cleaned_data["firstname"] = self.clean_username(
            cleaned_data.get("firstname"), "FirstName"
        )
        cleaned_data["lastname"] = self.clean_username(
            cleaned_data.get("lastname"), "LastName"
        )

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
            self.fields[field].widget.attrs["class"] = "form-control  text-dark"
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

    def clean_address(self):
        address = self.cleaned_data["address"]
        if not address:
            raise forms.ValidationError("Address is required.")
        return address

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number:
            raise forms.ValidationError("Phone number is required.")
        elif not str(phone_number).isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_city(self):
        city = self.cleaned_data["city"]
        if not city:
            raise forms.ValidationError("City is required.")
        return city

    def clean_district(self):
        state = self.cleaned_data["state"]
        if not state:
            raise forms.ValidationError("District is required.")
        return state

    def clean_country(self):
        country = self.cleaned_data["country"]
        if not country:
            raise forms.ValidationError("Country is required.")
        return country

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["placeholder"] = "Address "
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["city"].widget.attrs["placeholder"] = "City"
        self.fields["state"].widget.attrs["placeholder"] = "State"
        self.fields["country"].widget.attrs["placeholder"] = "Country"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control  text-dark"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"
