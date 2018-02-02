# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import Network, Location, Owner, Station

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

admin.site.register(Network, NetworkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Station, StationAdmin)