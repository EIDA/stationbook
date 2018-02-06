# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import\
get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from fdsn.fdsnStation.fdsnStation import StationList

from .models import Location, Owner, Network, Station

# Stations list view is used as a home screen for the Station Book
class HomeListView(ListView):
    model = Station
    context_object_name = 'stations'
    template_name = 'home.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Station.objects.all()
        return queryset

class LocationsListView(ListView):
    model = Location
    context_object_name = 'locations'
    template_name = 'locations.html'

    def get_queryset(self):
        queryset = Location.objects.all()
        return queryset

class OwnersListView(ListView):
    model = Owner
    context_object_name = 'owners'
    template_name = 'owners.html'

    def get_queryset(self):
        queryset = Owner.objects.all()
        return queryset

class NetworksListView(ListView):
    model = Network
    context_object_name = 'networks'
    template_name = 'networks.html'

    def get_queryset(self):
        queryset = Network.objects.order_by('name').all()
        return queryset

# Stations list view is used as a home screen for the Station Book
class StationsListView(ListView):
    model = Station
    context_object_name = 'stations'
    template_name = 'stations.html'

@method_decorator(login_required, name='dispatch')
class LocationDetailsListView(ListView):
    model = Location
    context_object_name = 'location'
    template_name = 'location_details.html'

@method_decorator(login_required, name='dispatch')
class OwnerDetailsListView(ListView):
    model = Owner
    context_object_name = 'owner'
    template_name = 'owner_details.html'

@method_decorator(login_required, name='dispatch')
class NetworkDetailsListView(ListView):
    model = Network
    context_object_name = 'network'
    template_name = 'network_details.html'

    def get_queryset(self):
        try:
            queryset = Network.objects.get(pk=self.kwargs.get('network_pk'))
        except Network.DoesNotExist:
            raise Http404("Network does not exist!")
        return queryset

@method_decorator(login_required, name='dispatch')
class StationDetailsListView(ListView):
    model = Station
    context_object_name = 'station'
    template_name = 'station_details.html'

    def get_queryset(self):
        try:
            queryset = Station.objects.get(pk=self.kwargs.get('station_pk'))
        except Station.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset

@method_decorator(login_required, name='dispatch')
class StationUpdateView(UpdateView):
    model = Station
    fields = ('code', 'name', 'affiliation', 'description', 'shared',
    'restricted', 'start', 'end', 'active')
    template_name = 'station_edit.html'
    pk_url_kwarg = 'station_pk'
    context_object_name = 'station'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        station = form.save(commit=False)
        station.save()
        return redirect('station_details', network_pk=station.station_network.pk, station_pk=station.pk)

def custom_404(request):
    return render_to_response('404.html')

def custom_500(request):
    return render_to_response('500.html')