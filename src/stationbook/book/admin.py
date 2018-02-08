# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import FdsnNetwork, FdsnStation, ExtBasicData, ExtOwnerData, \
                    ExtMorphologyData, ExtHousingData

class FdsnStationInline(admin.StackedInline):
    model = FdsnStation
    extra = 1

class FdsnNetworkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Change station details', {'fields': [
            'code', 'description', 'start_date', 'restricted_status',]}),
    ]
    inlines = [FdsnStationInline, ]
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

admin.site.register(FdsnNetwork, FdsnNetworkAdmin)
admin.site.register(FdsnStation, FdsnStationAdmin)