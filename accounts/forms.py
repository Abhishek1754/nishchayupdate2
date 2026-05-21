from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    referral_code_input = forms.CharField(
        required=False
    )

    class Meta:

        model = User

        fields = [

            'username',
            'email',
            'phone',
            'state',
            'pincode',
            'password',

        ]


class UserLoginForm(forms.Form):

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )