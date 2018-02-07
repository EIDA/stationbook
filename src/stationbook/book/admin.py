# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import Network, Location, Owner, Station, FdsnNetwork, FdsnStation

class StationInline(admin.TabularInline):
    model = Station
    extra = 1

class NetworkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change network details', {'fields': ['name', 'description',]}),
    ]
    inlines = [StationInline]
    list_display = ('name', 'description',)
    list_filter = ['name', 'description',]

class OwnerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change owner details', {'fields': ['owner_location', 'name',
        'department', 'agency', 'phone', 'email',]}),
    ]
    inlines = [StationInline]
    list_display = ('name',)
    list_filter = ['owner_location__name',]

class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change location details', {'fields': ['name', 'street', 'street_nr',
         'zip_code', 'city', 'country', 'latitude', 'longitude', 'elevation',]}),
        ]
    list_display = ('name', 'country', 'city', 'street',)
    list_filter = ['country', 'city',]

class StationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'station_network', 'station_location', 'station_owner',
            'code', 'name', 'affiliation', 'description', 'shared',
            'restricted', 'start', 'end', 'active']}),
    ]
    list_display = ('code', 'name', 'affiliation', 'description', 'shared',
    'restricted', 'start', 'end', 'active', 'installed_recently')
    list_filter = ['station_network__name', 'station_location__name',
    'station_owner__name', 'active',]

class FdsnStationInline(admin.StackedInline):
    model = FdsnStation
    extra = 1

class FdsnNetworkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'code', 'description', 'start_date', 'restricted_status',]}),
    ]
    inlines = [FdsnStationInline]
    list_display = ('code', 'description', 'start_date', 'restricted_status', )
    list_filter = ['description', 'code', ]

class FdsnStationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'code', 'site_name', 'latitude', 'longitude', 'elevation',
            'restricted_status', 'start_date', 'creation_date', ]}),
    ]
    list_display = ('code', 'site_name', 'latitude', 'longitude', 'elevation',
    'restricted_status', 'start_date', 'creation_date', )
    list_filter = ['fdsnStation_fdsnNetwork__code', ]

admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(FdsnNetwork, FdsnNetworkAdmin)
admin.site.register(FdsnStation, FdsnStationAdmin)