from django.contrib.auth.models import User
from .models import Profile, ExtBoreholeLayerData
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about', 'location', 'agency', 'department', 'telephone', 'skype', 'birth_date')

class NewBoreholeLayerForm(forms.ModelForm):
    class Meta:
        model = ExtBoreholeLayerData
        fields = ('description', 'depth_top', 'depth_bottom')