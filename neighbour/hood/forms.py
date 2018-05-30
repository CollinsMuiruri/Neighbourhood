from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, UserProfileModel, Profile, NeighbourhoodDetails, Business, Neighbourhood


class InfoImageForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['pub_date']
        widgets = {}


class ProfChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        exclude = ['pub_date']
        widgets = {}


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

        # validating the passwords
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password2'] != cd['password']:
                raise ValidationError("Passwords do not match")

            return cd['password2']


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class SocialDetailsForm(forms.ModelForm):
    class Meta:
        model = NeighbourhoodDetails
        exclude = ['neighbourhood']


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['neighbourhood', 'user']


class NewNeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        fields = ('neighbourhood_name', 'neighbourhood_location', 'neighbourhood_icon')
        exclude = ['occuupants_count', 'admin']
