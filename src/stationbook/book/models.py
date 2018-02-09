# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User

from django.utils.html import mark_safe
from markdown import markdown

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384

class ExtBasicData(models.Model):
    description = models.TextField(max_length=STRING_LENGTH_LONG)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))

class ExtOwnerData(models.Model):
    name = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    department = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    agency = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    street = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    country = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    phone = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    email = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')


class ExtMorphologyData(models.Model):
    description = models.TextField(max_length=STRING_LENGTH_LONG)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))


class ExtHousingData(models.Model):
    description = models.TextField(max_length=STRING_LENGTH_LONG)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))


class FdsnNetwork(models.Model):
    code = models.CharField(
        max_length=STRING_LENGTH_SHORT, unique=True, default='n/a')
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    start_date = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    restricted_status = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')

    def __str__(self):
        return self.code


class FdsnStation(models.Model):
    fdsnStation_fdsnNetwork = models.ForeignKey(
        FdsnNetwork, related_name='fdsn_stations',
        on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=STRING_LENGTH_SHORT, unique=True)
    site_name = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True)
    elevation = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True)
    restricted_status = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    start_date = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    creation_date = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    # Ext data
    ext_basic_data = models.OneToOneField(ExtBasicData,
        related_name='station', on_delete=models.CASCADE)
    ext_owner_data = models.OneToOneField(ExtOwnerData,
        related_name='station', on_delete=models.CASCADE)
    ext_morphology_data = models.OneToOneField(ExtMorphologyData,
        related_name='station', on_delete=models.CASCADE)
    ext_housing_data = models.OneToOneField(ExtHousingData,
        related_name='station', on_delete=models.CASCADE)

    def __str__(self):
        return self.code

    # @transaction.atomic
    # def save(self, *args, **kwargs):
    #     super(FdsnStation, self).save(*args, **kwargs)
    #     self.ext_basic_data.save()
    #     self.ext_owner_data.save()
    #     self.ext_morphology_data.save()
    #     self.ext_housing_data.save()

    # def installed_recently(self):
    #     today = datetime.date.today()
    #     return (today - datetime.timedelta(days=356) <= self.start)

    # installed_recently.admin_order_field = 'start'
    # installed_recently.boolean = True
    # installed_recently.short_description = 'Installed recently?'

class ExtAccessData(models.Model):
    extAccessData_fdsnStation = models.ForeignKey(FdsnStation,
        related_name='access_data', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(null=True)
    description = models.CharField(max_length=STRING_LENGTH_SHORT)

    def __str__(self):
        return '{0} has been updated at {1} by {2}: {3}'.format(
            self.extAccessData_fdsnStation__code,
            self.updated_at,
            self.updated_by,
            self.description)