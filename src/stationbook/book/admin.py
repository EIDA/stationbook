# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import FdsnNetwork, FdsnStation, ExtBasicData, \
                    ExtOwnerData, ExtMorphologyData, ExtHousingData, \
                    ExtBoreholeData, ExtBoreholeLayerData, Profile

class FdsnNetworkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'description', 'start_date', 'restricted_status',]}),
    ]
    list_display = ('code', 'description', 'start_date', 'restricted_status', )
    list_filter = ['description', 'code', ]

class FdsnStationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'site_name', 'latitude', 'longitude', 'elevation',
            'restricted_status', 'start_date', 'creation_date', ]}),
    ]
    list_display = ('code', 'site_name', 'latitude', 'longitude', 'elevation',
    'restricted_status', 'start_date', 'creation_date', )
    list_filter = [
        'fdsnStation_fdsnNetwork__description',
        'fdsnStation_fdsnNetwork__code',
    ]

class ExtBasicAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext basic details', {'fields': [
            'description', 'start', 'end',]}),
    ]
    list_display = ('__str__', 'description', 'start', 'end',)
    list_filter = ['station__fdsnStation_fdsnNetwork__code', 'station__code',]

class ExtOwnerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext owner details', {'fields': [
            'name_first', 'name_last', 'department', 'agency',
            'street', 'country', 'phone', 'email',]}),
    ]
    list_display = ('__str__', 'name_first', 'name_last', 'department',
    'agency', 'street', 'country', 'phone', 'email',)
    list_filter = ['station__fdsnStation_fdsnNetwork__code', 'station__code',]

class ExtMorphologyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext morphology details', {'fields': [
            'description', 'geological_unit', 'morphology_class',
            'ground_type_ec8', 'groundwater_depth', 'vs_30', 'f0',
            'amp_f0', 'basin_flag', 'bedrock_depth',]}),
    ]
    list_display = ('__str__', 'description', 'geological_unit',
    'morphology_class', 'ground_type_ec8', 'groundwater_depth', 'vs_30', 'f0',
    'amp_f0', 'basin_flag', 'bedrock_depth',)
    list_filter = ['station__fdsnStation_fdsnNetwork__code', 'station__code',]

class ExtHousingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext housing details', {'fields': [
            'description', 'housing_class', 'in_building',
            'numer_of_storeys','distance_to_building',]}),
    ]
    list_display = ('__str__', 'description', 'housing_class', 'in_building',
    'numer_of_storeys','distance_to_building',)
    list_filter = ['station__fdsnStation_fdsnNetwork__code', 'station__code',]

class ExtBoreholeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext borehole details', {'fields': ['depth',]}),
    ]
    list_display = ('__str__', 'depth',)
    list_filter = ['station__fdsnStation_fdsnNetwork__code', 'station__code',]

class ExtBoreholeLayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change ext borehole details', {'fields': [
            'description', 'depth_top', 'depth_bottom',]}),
    ]
    list_display = ('description', 'depth_top', 'depth_bottom',)

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change profile details', {'fields': [
            'about', 'location', 'birth_date',]}),
    ]
    list_display = ('__str__', 'user', 'about', 'location', 'birth_date',)

admin.site.register(FdsnNetwork, FdsnNetworkAdmin)
admin.site.register(FdsnStation, FdsnStationAdmin)
admin.site.register(ExtBasicData, ExtBasicAdmin)
admin.site.register(ExtOwnerData, ExtOwnerAdmin)
admin.site.register(ExtMorphologyData, ExtMorphologyAdmin)
admin.site.register(ExtHousingData, ExtHousingAdmin)
admin.site.register(ExtBoreholeData, ExtBoreholeAdmin)
admin.site.register(Profile, ProfileAdmin)