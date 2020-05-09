from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "Password missmatch",
    }

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-box", "placeholder": "Username"}),
        required=True,
        max_length=100,
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "input-box", "placeholder": "Email"}),
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input-box", "placeholder": "Password"}
        ),
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input-box", "placeholder": "Confirm Password"}
        ),
        required=True,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "profile-input-box", "placeholder": "Username"}
        ),
        required=True,
        max_length=100,
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "profile-input-box", "placeholder": "Email"}
        ),
        required=True,
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-box", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input-box", "placeholder": "Password"}
        )
    )
