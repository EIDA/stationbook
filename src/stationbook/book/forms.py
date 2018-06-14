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
            'site_name',
            'latitude_min',
            'latitude_max',
            'longitude_min',
            'longitude_max',
            'start_year_from',
            'start_year_to',
            'end_year_from',
            'end_year_to',
            'geological_unit',
            'morphology_class',
            'ground_type_ec8',
        )
        labels = {
            'network_code': 'Network Code',
            'station_code': 'Station Code',
            'site_name': 'Site name',
            'latitude_min': 'Latitude minimum',
            'latitude_max': 'Latitude maximum',
            'longitude_min': 'Longitude minimum',
            'longitude_max': 'Longitude maximum',
            'start_year_from': 'Start year from',
            'start_year_to': 'Start year to',
            'end_year_from': 'End year from',
            'end_year_to': 'End year to',
            'geological_unit': 'Geological unit',
            'morphology_class': 'Morphology class',
            'ground_type_ec8': 'Ground type EC8',
        }
