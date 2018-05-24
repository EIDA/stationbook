# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import FdsnNode, FdsnNetwork, FdsnStation, ExtBasicData, \
                    ExtOwnerData, ExtMorphologyData, ExtHousingData, \
                    ExtBoreholeData, ExtBoreholeLayerData, Profile, Photo, Link


class FdsnNodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change node details', {
                'fields': [
                    'code',
                    'description',
                    'url_dataselect',
                    'url_station',
                    'url_routing',
                    'url_wfcatalog',
                ]
            }
        ),
    ]

    list_display = (
        'code',
        'description',
        'url_dataselect',
        'url_station',
        'url_routing',
        'url_wfcatalog',
    )

    list_filter = [
        'code',
        'description',
    ]

    search_fields = [
        'code',
    ]


class FdsnNetworkAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change station details', {
                'fields': [
                    'description',
                    'restricted_status',
                ]
            }
        ),
    ]

    list_display = (
        'fdsn_node',
        'code',
        'description',
        'start_date',
        'restricted_status', 
    )

    list_filter = [
        'fdsn_node__code',
        'code',
    ]

    search_fields = [
        'code',
    ]


class FdsnStationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change station details', {
                'fields': [
                    'site_name',
                    'latitude',
                    'longitude',
                    'elevation',
                    'restricted_status',
                    'start_date',
                    'creation_date',
                ]
            }
        ),
    ]

    list_display = (
        'fdsn_network',
        'code',
        'site_name',
        'latitude',
        'longitude',
        'elevation',
        'restricted_status',
        'start_date',
        'creation_date',
    )

    list_filter = [
        'fdsn_network__fdsn_node__code',
        'fdsn_network__code',
    ]

    search_fields = [
        'code',
    ]


class ExtBasicAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext basic details', {
                'fields': [
                    'description',
                    'start',
                    'end',
                    'imported_from_fdsn',
                    'last_synced',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'description',
        'start',
        'end',
        'imported_from_fdsn',
        'last_synced',
    )

    list_filter = [
        'station__fdsn_network__code',
    ]

    search_fields = [
        'station__code',
    ]


class ExtOwnerAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext owner details', {
                'fields': [
                    'name_first',
                    'name_last',
                    'department',
                    'agency',
                    'street',
                    'country',
                    'phone',
                    'email',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'name_first',
        'name_last',
        'department',
        'agency',
        'street',
        'country',
        'phone',
        'email',
    )

    list_filter = [
        'station__fdsn_network__code',
        'station__code',
    ]

    search_fields = [
        'station__code',
    ]


class ExtMorphologyAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext morphology details', {
                'fields': [
                    'description',
                    'geological_unit',
                    'morphology_class',
                    'ground_type_ec8',
                    'groundwater_depth',
                    'vs_30',
                    'f0',
                    'amp_f0',
                    'basin_flag',
                    'bedrock_depth',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'description',
        'geological_unit',
        'morphology_class',
        'ground_type_ec8',
        'groundwater_depth',
        'vs_30',
        'f0',
        'amp_f0',
        'basin_flag',
        'bedrock_depth',
    )

    list_filter = [
        'station__fdsn_network__code',
        'station__code',
    ]

    search_fields = [
        'station__code',
    ]


class ExtHousingAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext housing details', {
                'fields': [
                    'description',
                    'housing_class',
                    'in_building',
                    'numer_of_storeys',
                    'distance_to_building',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'description',
        'housing_class',
        'in_building',
        'numer_of_storeys',
        'distance_to_building',
    )

    list_filter = [
        'station__fdsn_network__code',
        'station__code',
    ]

    search_fields = [
        'station__code',
    ]


class ExtBoreholeAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext borehole details', {
                'fields': [
                    'depth',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'depth',
    )

    list_filter = [
        'station__fdsn_network__code',
        'station__code',
    ]

    search_fields = [
        'station__code',
    ]


class ExtBoreholeLayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change ext borehole details', {
                'fields': [
                    'description',
                    'depth_top',
                    'depth_bottom',
                ]
            }
        ),
    ]

    list_display = (
        'description',
        'depth_top',
        'depth_bottom',
    )

    list_filter = [
        'borehole_data__station__fdsn_network__code', 
        'borehole_data__station__code',
    ]

    search_fields = [
        'borehole_data__station__code',
    ]


class PhotoAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change photo details', {
                'fields': [
                    'description',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'description',
        'photo',
        'uploaded_at',
    )

    list_filter = [
        'fdsn_station__fdsn_network__code',
        'fdsn_station__code',
    ]

    search_fields = [
        'fdsn_station__code',
    ]


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change profile details', {
                'fields': [
                    'fdsn_networks',
                    'about',
                    'location',
                    'agency',
                    'department',
                    'telephone',
                    'skype',
                    'birth_date',
                ]
            }
        ),
    ]

    list_display = (
        '__str__',
        'user',
        'about',
        'location',
        'birth_date',
    )


class LinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Change link details', {
                'fields': [
                    'url',
                    'category',
                    'description',
                ]
            }
        ),
    ]

    list_display = (
        'url',
        'category',
        'description',
    )

# Register the models on the admin site
admin.site.register(FdsnNode, FdsnNodeAdmin)
admin.site.register(FdsnNetwork, FdsnNetworkAdmin)
admin.site.register(FdsnStation, FdsnStationAdmin)
admin.site.register(ExtBasicData, ExtBasicAdmin)
admin.site.register(ExtOwnerData, ExtOwnerAdmin)
admin.site.register(ExtMorphologyData, ExtMorphologyAdmin)
admin.site.register(ExtHousingData, ExtHousingAdmin)
admin.site.register(ExtBoreholeData, ExtBoreholeAdmin)
admin.site.register(ExtBoreholeLayerData, ExtBoreholeLayerAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Link, LinkAdmin)