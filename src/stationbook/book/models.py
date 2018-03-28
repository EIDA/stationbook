# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models, transaction
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from markdown import markdown

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384

class ExtEntityBase(models.Model):
    # TODO: entities should not be removed. It is more mature to set 'removed'
    # flag to true and filter them out in the queries.
    entity_removed = models.BooleanField(default=False)


class ExtBasicData(ExtEntityBase):
    description = models.TextField(
        max_length=STRING_LENGTH_LONG, default='', blank=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    imported_from_fdsn = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Basic data for station {0}'.format(self.station.code)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))


class ExtOwnerData(ExtEntityBase):
    name_first = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    name_last = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    department = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    agency = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    city = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    street = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    country = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    phone = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')
    email = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True, default='n/a')

    def __str__(self):
        return 'Owner data for station {0}'.format(self.station.code)


class ExtMorphologyData(ExtEntityBase):
    GEOLOGICAL_UNIT_CHOICES = (
        ('unknown', 'Unknown'),
        ('alluvial_deposits', 'Alluvial deposits'),
        ('ancient_alluvialterraces', 'Ancient alluvial terraces'),
        ('argillite', 'Argillite'),
        ('breccias', 'Breccias'),
        ('clay', 'Clay'),
        ('conglomerate', 'Conglomerate'),
        ('debris', 'Debris'),
        ('diabase', 'Diabase'),
        ('dolomite', 'Dolomite'),
        ('fillade', 'Fillade'),
        ('fluvial_deposits', 'Fluvial deposits'),
        ('gneiss', 'Gneiss'),
        ('granite', 'Granite'),
        ('jasper', 'Jasper'),
        ('lacustrine_deposits', 'Lacustrine deposits'),
        ('limestone', 'Limestone'),
        ('marls', 'Marls'),
        ('metamorphic_rock', 'Metamorphic rock'),
        ('micaschist', 'Micaschist'),
        ('morainic_deposits', 'Morainic deposits'),
        ('ophiolite', 'Ophiolite'),
        ('rhyolitic_ignimbrite', 'Rhyolitic ignimbrite'),
        ('sand_deposits', 'Sand deposits'),
        ('sandstone', 'Sandstone'),
        ('schist', 'Schist'),
        ('torbidite', 'Torbidite'),
        ('volcanic_deposits', 'Volcanic deposits'),
        ('volcanic_rocks', 'Volcanic rocks'),
    )

    MORPHOLOGY_CLASS_CHOICES = (
        ('unknown', 'Unknown'),
        ('t1', 'T1'),
        ('t2', 'T2'),
        ('t3', 'T3'),
        ('t4', 'T4'),
    )

    GROUND_TYPE_EC8_CHOICES = (
        ('unknown', 'Unknown'),
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
        ('s1', 'S1'),
        ('s2', 'S2'),
    )

    description = models.TextField(
        max_length=STRING_LENGTH_LONG, default='', blank=True)
    geological_unit = models.CharField(
        max_length=STRING_LENGTH_SHORT,
        choices=GEOLOGICAL_UNIT_CHOICES,
        default='', blank=True)
    morphology_class = models.CharField(
        max_length=STRING_LENGTH_SHORT,
        choices=MORPHOLOGY_CLASS_CHOICES,
        default='', blank=True)
    ground_type_ec8 = models.CharField(
        max_length=STRING_LENGTH_SHORT,
        choices=GROUND_TYPE_EC8_CHOICES,
        default='', blank=True)
    groundwater_depth = models.IntegerField(default=0)
    vs_30 = models.IntegerField(default=0)
    f0 = models.IntegerField(default=0)
    amp_f0 = models.IntegerField(default=0)
    basin_flag =  models.BooleanField(default=False)
    bedrock_depth = models.IntegerField(default=0)

    def __str__(self):
        return 'Morphology data for station {0}'.format(self.station.code)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))


class ExtHousingData(ExtEntityBase):
    HOUSING_CLASS_CHOICES = (
        ('borehole', 'Borehole'),
        ('bridge', 'Bridge'),
        ('building', 'Building'),
        ('cave', 'Cave'),
        ('dam', 'Dam'),
        ('free_field', 'Free field'),
        ('other_structure', 'Other structure'),
        ('tunnel', 'Tunnel'),
        ('underground_shelter', 'Underground shelter'),
        ('urban_free_field', 'Urban free field'),
    )

    description = models.TextField(
        max_length=STRING_LENGTH_LONG, default='', blank=True)
    housing_class = models.CharField(
        max_length=STRING_LENGTH_SHORT,
        choices=HOUSING_CLASS_CHOICES,
        default='', blank=True)
    in_building = models.BooleanField(default=True)
    numer_of_storeys = models.IntegerField(default=0)
    distance_to_building = models.IntegerField(default=0)

    def __str__(self):
        return 'Housing data for station {0}'.format(self.station.code)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))


class ExtBoreholeData(ExtEntityBase):
    depth = models.IntegerField(default=0)

    def __str__(self):
        return 'Borehole data for station {0}'.format(self.station.code)


class ExtBoreholeLayerData(ExtEntityBase):
    borehole_data = models.ForeignKey(
        ExtBoreholeData, related_name='borehole_layers', 
        null=True, on_delete=models.SET_NULL)
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)
    depth_top = models.IntegerField(default=0)
    depth_bottom = models.IntegerField(default=0)

    def __str__(self):
        return self.borehole_data.station.code


class FdsnNode(models.Model):
    code = code = models.CharField(
        primary_key=True, max_length=STRING_LENGTH_SHORT, unique=True)
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)
    url_dataselect = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_station = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_routing = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_wfcatalog = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    
    def __str__(self):
        return self.code


class FdsnNetwork(models.Model):
    fdsn_node = models.ForeignKey(
        FdsnNode, related_name='fdsn_networks',
        on_delete=models.CASCADE, default=None)
    code = models.CharField(
        max_length=STRING_LENGTH_SHORT)
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)
    start_date = models.DateTimeField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)
    restricted_status = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)

    class Meta:
        unique_together = (('fdsn_node', 'code', 'start_date'),)
        ordering = ['fdsn_node__code', 'code',]

    def __str__(self):
        return 'Node {0} Network {1} Year {2}'.format(
            self.fdsn_node.code,
            self.code,
            self.start_date.year)
    
    def has_stations(self):
        return self.fdsn_stations.count > 0
    
    def get_code_year(self):
        return '{0} {1}'.format(self.code, self.start_date.year)
    
    def get_start_date(self):
        return '{0}/{1}/{2}'.format(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day
        )


class FdsnStation(models.Model):
    fdsn_network = models.ForeignKey(
        FdsnNetwork, related_name='fdsn_stations',
        on_delete=models.CASCADE, default=None)
    code = models.CharField(
        max_length=STRING_LENGTH_SHORT)
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
    start_date = models.DateTimeField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    end_date = models.DateTimeField(
        max_length=STRING_LENGTH_SHORT, null=True, blank=True)
    creation_date = models.DateTimeField(
        max_length=STRING_LENGTH_SHORT, blank=True)
    # Ext data
    ext_basic_data = models.OneToOneField(ExtBasicData,
        related_name='station', null=True, on_delete=models.SET_NULL)
    ext_owner_data = models.OneToOneField(ExtOwnerData,
        related_name='station', null=True, on_delete=models.SET_NULL)
    ext_morphology_data = models.OneToOneField(ExtMorphologyData,
        related_name='station', null=True, on_delete=models.SET_NULL)
    ext_housing_data = models.OneToOneField(ExtHousingData,
        related_name='station', null=True, on_delete=models.SET_NULL)
    ext_borehole_data = models.OneToOneField(ExtBoreholeData,
        related_name='station', null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (('fdsn_network', 'code', 'start_date'),)
        ordering = ['fdsn_network__fdsn_node__code', 'fdsn_network__code', 'code',]

    def __str__(self):
        return 'Station {0}'.format(self.code)
    
    def get_start_date(self):
        return '{0}/{1}/{2}'.format(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day
        )
    
    def get_end_date(self):
        if self.end_date:
            return '{0}/{1}/{2}'.format(
                self.end_date.year,
                self.end_date.month,
                self.end_date.day
            )
        else:
            return None
    
    def get_created_date(self):
        return '{0}/{1}/{2}'.format(
            self.creation_date.year,
            self.creation_date.month,
            self.creation_date.day
        )


class ExtAccessData(ExtEntityBase):
    fdsn_station = models.ForeignKey(FdsnStation,
        related_name='access_data', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(null=True)
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='Change', blank=True)

    class Meta:
        ordering = ['-updated_at',]

    def __str__(self):
        return '{0} has been updated at {1} by {2}: {3}'.format(
            self.fdsn_station.code,
            self.updated_at,
            self.updated_by,
            self.description)


class Photo(models.Model):
    def path_file_name(self, instance):
        return 'station_photos/{0}-{1}/{2}-{3}/{4}'.format(
            self.fdsn_station.fdsn_network.code,
            self.fdsn_station.fdsn_network.start_date.year,
            self.fdsn_station.code,
            self.fdsn_station.start_date.year,
            self.fdsn_station.code
            )

    fdsn_station = models.ForeignKey(
        FdsnStation, related_name='photos', on_delete=models.CASCADE)
    description = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    photo = models.ImageField(upload_to=path_file_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at',]

    def __str__(self):
        return 'Station {0}, photo description: {1}'.format(
            self.fdsn_station.code,
            self.description
        )


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    fdsn_networks = models.ManyToManyField(FdsnNetwork, blank=True, related_name='editors')
    about = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    location = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    agency = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    department = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    telephone = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    skype = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Profile of: {0}'.format(self.user)


class Link(models.Model):
    url = models.CharField(max_length=STRING_LENGTH_MEDIUM, null=True, blank=True)
    category = models.CharField(max_length=STRING_LENGTH_MEDIUM, null=True, blank=True)
    description = models.CharField(max_length=STRING_LENGTH_MEDIUM, null=True, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(
            self.url,
            self.description
        )