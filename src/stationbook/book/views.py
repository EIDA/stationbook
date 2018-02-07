# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from fdsn.fdsnStation.fdsnStation import NetworkStationGraph

from .models import Location, Owner, Network, Station, FdsnNetwork, FdsnStation
from fdsn.fdsnStation.fdsnStation import NetworkStationGraph

# Stations list view is used as a home screen for the Station Book
class HomeListView(ListView):
    model = FdsnStation
    context_object_name = 'stations'
    template_name = 'home.html'
    paginate_by = 5

    def get_queryset(self):
        # refresh_fdsn()
        queryset = FdsnStation.objects.all()
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
    model = FdsnNetwork
    context_object_name = 'network'
    template_name = 'network_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnNetwork.objects.get(pk=self.kwargs.get('network_pk'))
        except FdsnNetwork.DoesNotExist:
            raise Http404("Network does not exist!")
        return queryset

@method_decorator(login_required, name='dispatch')
class StationDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnStation.objects.get(pk=self.kwargs.get('station_pk'))
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset

@method_decorator(login_required, name='dispatch')
class StationUpdateView(UpdateView):
    model = FdsnStation
    fields = ('code', 'site_name', 'latitude', 'longitude', 'elevation',
    'restricted_status', 'start_date', 'creation_date')
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

def refresh_fdsn():
    try:
        FdsnNetwork.objects.all().delete()
        data = NetworkStationGraph('*')
        graph = data.get_network_station_graph()
        for network in graph.networks:
            net = FdsnNetwork()
            net.code = network.code
            net.name = network.name
            net.description = network.description
            net.start_date = network.start_date
            net.restricted_status = network.restricted_status
            print('Network:' + net.code)
            # If network is not known in the database, add it, otherwise get it
            #  from the database to prevent operating on a detached entity
            if not FdsnNetwork.objects.filter(code=net.code).exists():
                net.save()
            else:
                net = FdsnNetwork.objects.get(code=net.code)
            for station in network.stations:
                stat = FdsnStation()
                stat.fdsnStation_fdsnNetwork = net
                stat.code = station.code
                stat.latitude = station.latitude
                stat.longitude = station.longitude
                stat.elevation = station.elevation
                stat.restricted_status = station.restricted_status
                stat.start_date = station.start_date
                stat.creation_date = station.creation_date
                stat.site_name = station.site_name
                print('Station: ' + stat.code)
                # In case station data appears twice in the same dataset,
                # ignore it
                if not FdsnStation.objects.filter(code=net.code).exists():
                    stat.save()
    except:
        raise