from django.contrib.auth.models import User
from .models import \
    Profile, ExtBoreholeLayerData, Photo, SearchFdsnStationModel
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'about', 'location', 'agency', 'department', 
            'telephone', 'skype', 'birth_date'
            )


class AddBoreholeLayerForm(forms.ModelForm):
    class Meta:
        model = ExtBoreholeLayerData
        fields = ('description', 'depth_top', 'depth_bottom')


class EditBoreholeLayerForm(forms.ModelForm):
    class Meta:
        model = ExtBoreholeLayerData
        fields = ('description', 'depth_top', 'depth_bottom')


class RemoveBoreholeLayerForm(forms.ModelForm):
    class Meta:
        model = ExtBoreholeLayerData
        fields = ('description', 'depth_top', 'depth_bottom')


class StationPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'photo', )


class StationPhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description',)


class StationPhotoRemoveForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description',)


class SearchAdvancedForm(forms.ModelForm):
    class Meta:
        model = SearchFdsnStationModel
        fields = (
            'network_code',
            'station_code',
        )
        labels = {
            'network_code': 'FDSN Network Code',
            'station_code': 'FDSN Station Code',
        }
