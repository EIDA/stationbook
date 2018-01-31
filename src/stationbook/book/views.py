# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import UpdateView, ListView
from fdsn.fdsnStation.fdsnStation import StationList

from .models import Station

class StationListView(ListView):
    model = Station
    context_object_name = 'stations'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stat_list = StationList('nl')
        stat_collection = stat_list.get_station_collection()
        context['stations'] = stat_collection
        return context
