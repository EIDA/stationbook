from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about', 'location', 'birth_date')