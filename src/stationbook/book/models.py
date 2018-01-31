# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name