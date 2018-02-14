# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
from functools import reduce

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, \
render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q

from .fdsn.station import refresh_station_in_thread
from .models import FdsnNetwork, FdsnStation, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, \
ExtHousingData, ExtAccessData, ExtBoreholeData, ExtBoreholeLayerData
from .book_base_classes import StationUpdateViewBase
from .logger import StationBookLogger

# Stations list view is used as a home screen for the Station Book
class HomeListView(ListView):
    model = FdsnStation
    context_object_name = 'stations'
    template_name = 'home.html'

    def get_queryset(self):
        queryset = FdsnStation.objects.order_by('?')[:1]
        return queryset


class SearchListView(ListView):
    model = FdsnStation
    context_object_name = 'data'
    template_name = 'search.html'

    def get_queryset(self):
        if self._get_search_phrase() == None:
            queryset = None
        else:
            queryset = FdsnStation.objects.all()

        query = self.request.GET.get('search_text')
        if query:
            query_list = query.split()
            queryset = queryset.filter(
                reduce(operator.and_, (
                    Q(code__icontains=q) for q in query_list)) | 
                reduce(operator.and_,(
                    Q(site_name__icontains=q) for q in query_list)))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_phrase'] = self._get_search_phrase()
        return context

    def _get_search_phrase(self):
        return ((lambda x: x if len(x) > 0 else None)(
            self.request.GET.get('search_text', '')))

class NetworksListView(ListView):
    model = FdsnNetwork
    context_object_name = 'data'
    template_name = 'networks.html'

    def get_queryset(self):
        queryset = FdsnNetwork.objects.all().order_by('code')
        return queryset


class RecentChangesListView(ListView):
    model = ExtAccessData
    context_object_name = 'data'
    template_name = 'recent_changes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = ExtAccessData.objects.order_by('-updated_at')[:1000]
        return queryset


class NetworkDetailsListView(ListView):
    model = FdsnNetwork
    context_object_name = 'network'
    template_name = 'network_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnNetwork.objects.\
            get(code=self.kwargs.get('network_code'))
        except FdsnNetwork.DoesNotExist:
            raise Http404("Network does not exist!")
        return queryset


class StationDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnStation.objects.\
            get(code=self.kwargs.get('station_code'))
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fdsn_station_link'] = \
        'http://orfeus-eu.org/fdsnws/station/1/query?network={net}&station={stat}&level=channel'\
        .format(net=self.kwargs.get('network_code'), stat=self.kwargs.get('station_code'))
        return context


class StationGalleryListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_gallery.html'

    def get_queryset(self):
        try:
            queryset = FdsnStation.objects.\
            get(code=self.kwargs.get('station_code'))
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset


@method_decorator(login_required, name='dispatch')
class ExtBasicDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
        model=ExtBasicData,
        fields=('description', 'start', 'end',))

    def get_object(self):
        obj = get_object_or_404(self.model, \
        station__code=self.kwargs['station_code'])
        return obj

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        print(data.station)
        self.add_ext_access_data(data.station, 'Updated basic data')
        return redirect('station_details', \
        network_code=data.station.fdsnStation_fdsnNetwork.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtOwnerDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
        model=ExtOwnerData,
        fields=('name_first', 'name_last', 'department', 'agency',
        'street', 'country', 'phone', 'email',))

    def get_object(self):
        obj = get_object_or_404(self.model, \
        station__code=self.kwargs['station_code'])
        return obj

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        self.add_ext_access_data(data.station, 'Updated owner data')
        return redirect('station_details', \
        network_code=data.station.fdsnStation_fdsnNetwork.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtMorphologyDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
        model=ExtMorphologyData,
        fields=('description', 'geological_unit', 'morphology_class',
        'ground_type_ec8', 'groundwater_depth', 'vs_30', 'f0', 'amp_f0',
        'basin_flag', 'bedrock_depth',))

    def get_object(self):
        obj = get_object_or_404(self.model, \
        station__code=self.kwargs['station_code'])
        return obj

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        self.add_ext_access_data(data.station, 'Updated morphology data')
        return redirect('station_details', \
        network_code=data.station.fdsnStation_fdsnNetwork.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtHousingDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
            model=ExtHousingData,
            fields=('description', 'housing_class', 'in_building',
            'numer_of_storeys', 'distance_to_building',))

    def get_object(self):
        obj = get_object_or_404(self.model, \
        station__code=self.kwargs['station_code'])
        return obj

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        self.add_ext_access_data(data.station, 'Updated housing data')
        return redirect('station_details', \
        network_code=data.station.fdsnStation_fdsnNetwork.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtBoreholeDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
            model=ExtBoreholeData,
            fields=('depth',))

    def get_object(self):
        obj = get_object_or_404(self.model, \
        station__code=self.kwargs['station_code'])
        return obj

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        self.add_ext_access_data(data.station, 'Updated borehole data')
        return redirect('station_details', \
        network_code=data.station.fdsnStation_fdsnNetwork.code, \
        station_code=data.station.code)

def custom_404(request):
    return render_to_response('404.html')

def custom_500(request):
    return render_to_response('500.html')

@user_passes_test(lambda u: u.is_superuser)
def refresh_fdsn(request):
    StationBookLogger(__name__).log_info(
        'Refreshing FDSN by {0}'.format(request.user))
    refresh_station_in_thread()
    return redirect('home')