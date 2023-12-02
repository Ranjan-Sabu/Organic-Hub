from django import forms
from .models import Registration

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



    def clean(self):
        cleaned_data = super(Registrationform,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirmpassword')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match.'
            )