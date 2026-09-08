from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "profile_picture",
            "bio",
            "phone",
            "college",
        )