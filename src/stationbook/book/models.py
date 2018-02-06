# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

STRING_LENGTH_SHORT = 256
STRING_LENGTH_LONG = 1024

class Network(models.Model):
    name = models.CharField(max_length=STRING_LENGTH_SHORT, unique=True)
    description = models.CharField(max_length=STRING_LENGTH_SHORT)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=STRING_LENGTH_LONG)
    street = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    street_nr = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    zip_code = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    city = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    country = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return self.name

class Owner(models.Model):
    owner_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    department = models.CharField(max_length=STRING_LENGTH_LONG, blank=True)
    agency = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)
    phone = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)
    email = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)

    def __str__(self):
        return self.name

class Station(models.Model):
    station_network = models.ForeignKey(
        Network, related_name='stations', on_delete=models.CASCADE, default=None)
    station_location = models.ForeignKey(
        Location, related_name='stations', on_delete=models.CASCADE, default=None)
    station_owner = models.ForeignKey(
        Owner, related_name='stations', on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=STRING_LENGTH_SHORT, unique=True)
    name = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)
    affiliation = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)
    description = models.CharField(max_length=STRING_LENGTH_SHORT, blank=True)
    shared = models.BooleanField()
    restricted = models.BooleanField()
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.name

    def installed_recently(self):
        today = datetime.date.today()
        return (today - datetime.timedelta(days=356) <= self.start)

    installed_recently.admin_order_field = 'start'
    installed_recently.boolean = True
    installed_recently.short_description = 'Installed recently?'