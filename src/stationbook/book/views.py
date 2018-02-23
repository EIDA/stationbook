# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
from functools import reduce

from django.http import Http404
from django.shortcuts import \
get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.db.models import Q

from .fdsn.station import refresh_station_in_thread
from .fdsn.station_channels import StationChannelsGraph
from .models import \
FdsnNetwork, FdsnStation, ExtBasicData, ExtOwnerData, ExtMorphologyData, \
ExtHousingData, ExtAccessData, ExtBoreholeData, ExtBoreholeLayerData, Photo

from .base_classes import \
StationBookHelpers, StationUpdateViewBase, StationAccessManager

from .logger import StationBookLogger
from .forms import \
UserForm, ProfileForm, AddBoreholeLayerForm, RemoveBoreholeLayerForm, \
StationPhotoForm, StationPhotoEditForm, StationPhotoRemoveForm

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
    paginate_by = 10
    
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
            queryset = FdsnStation.objects.get(
                fdsn_network__code=self.kwargs.get('network_code'),
                code=self.kwargs.get('station_code'))
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fdsn_station_link'] = \
        'http://orfeus-eu.org/fdsnws/station/1/query?network={net}&station={stat}&level=channel'\
        .format(
            net=self.kwargs.get('network_code'),
            stat=self.kwargs.get('station_code'))

        scg = StationChannelsGraph(
            network=self.kwargs.get('network_code'),
            station=self.kwargs.get('station_code'))
        scg_result = scg.get_station_channels()
        context['station_channels'] = scg_result.channels

        user_is_network_editor = \
        StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network=FdsnNetwork.objects.get(
                code=self.kwargs.get('network_code')))
        context['user_is_network_editor'] = user_is_network_editor
        return context


class StationGalleryListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_gallery.html'

    def get_queryset(self):
        try:
            queryset = FdsnStation.objects.\
            get(fdsn_network__code=self.kwargs['network_code'],
                code=self.kwargs.get('station_code'))
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
        self.ensure_user_access_right()
        obj = get_object_or_404(self.model, \
        station__fdsn_network__code=self.kwargs['network_code'],
        station__code=self.kwargs['station_code'])
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        print(data.station)

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated basic data')

        return redirect('station_details', \
        network_code=data.station.fdsn_network.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtOwnerDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
        model=ExtOwnerData,
        fields=('name_first', 'name_last', 'department', 'agency',
        'street', 'country', 'phone', 'email',))

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(self.model, \
        station__fdsn_network__code=self.kwargs['network_code'],
        station__code=self.kwargs['station_code'])
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated owner data')

        return redirect('station_details', \
        network_code=data.station.fdsn_network.code, \
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
        self.ensure_user_access_right()
        obj = get_object_or_404(self.model, \
        station__fdsn_network__code=self.kwargs['network_code'],
        station__code=self.kwargs['station_code'])
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated morphology data')

        return redirect('station_details', \
        network_code=data.station.fdsn_network.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtHousingDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
            model=ExtHousingData,
            fields=('description', 'housing_class', 'in_building',
            'numer_of_storeys', 'distance_to_building',))

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(self.model, \
        station__fdsn_network__code=self.kwargs['network_code'],
        station__code=self.kwargs['station_code'])
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated housing data')

        return redirect('station_details', \
        network_code=data.station.fdsn_network.code, \
        station_code=data.station.code)


@method_decorator(login_required, name='dispatch')
class ExtBoreholeDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(self, 
            model=ExtBoreholeData,
            fields=('depth',))

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(self.model, \
        station__fdsn_network__code=self.kwargs['network_code'],
        station__code=self.kwargs['station_code'])
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated borehole data')

        return redirect('station_details', \
        network_code=data.station.fdsn_network.code, \
        station_code=data.station.code)


@login_required
@transaction.atomic
def station_borehole_layer_add(request, network_code, station_code):
    station = get_object_or_404(
        FdsnStation, fdsn_network__code=network_code, code=station_code)
    
    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = AddBoreholeLayerForm(request.POST)
        if form.is_valid():
            borehole_layer = form.save(commit=False)
            borehole_layer.borehole_data = station.ext_borehole_data
            borehole_layer.save()

            StationBookHelpers.add_ext_access_data(
                request.user, station,
                'Added borehole layer ({0})'.format(
                    borehole_layer.description))

            return redirect('station_details', \
                network_code=network_code, \
                station_code=station_code)
    else:
        form = AddBoreholeLayerForm()
        return render(
            request, 'station_borehole_layer_add.html',
            {'station': station, 'form': form})


@login_required
@transaction.atomic
def station_borehole_layer_remove(request, network_code, station_code, pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__code=network_code, code=station_code)
    borehole_layer = get_object_or_404(
        ExtBoreholeLayerData, pk=pk)
    
    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = RemoveBoreholeLayerForm(request.POST)
        ExtBoreholeLayerData.objects.get(pk=pk).delete()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Removed borehole layer ({0})'.format(
                borehole_layer.description))

        return redirect('station_details', \
            network_code=network_code, \
            station_code=station_code)
    else:
        form = RemoveBoreholeLayerForm()
        return render(
            request, 'station_borehole_layer_rem.html',
            {'station': station, 'layer': borehole_layer, 'form': form})


@login_required
@transaction.atomic
def station_photo_upload(request, network_code, station_code):
    station = get_object_or_404(
        FdsnStation, fdsn_network__code=network_code, code=station_code)
    
    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.fdsn_station = station
            photo.save()

            StationBookHelpers.add_ext_access_data(
                request.user, station,
                'Added photo ({0})'.format(photo.description))

            return redirect('station_gallery', \
                network_code=network_code, \
                station_code=station_code)
    else:
        form = StationPhotoForm()
        return render(request, 'upload_photo.html', {
            'station': station, 'form': form})


@login_required
@transaction.atomic
def station_photo_edit(request, network_code, station_code, pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__code=network_code, code=station_code)
    photo = get_object_or_404(Photo, pk=pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoEditForm(request.POST, instance=photo)
        form.save()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Photo edited ({0})'.format(
                photo.description))
        
        return redirect('station_gallery',
            network_code=network_code,
            station_code=station_code)
    else:
        form = StationPhotoEditForm(instance=photo)
        return render(request, 'station_gallery_photo_edit.html', {
            'station': station, 'img': photo, 'form': form
            })


@login_required
@transaction.atomic
def station_photo_remove(request, network_code, station_code, pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__code=network_code, code=station_code)
    photo = get_object_or_404(Photo, pk=pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoRemoveForm(request.POST, instance=photo)
        Photo.objects.get(pk=pk).delete()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Removed photo ({0})'.format(
                photo.description))
        
        return redirect('station_gallery',
            network_code=network_code,
            station_code=station_code)
    else:
        form = StationPhotoRemoveForm(instance=photo)
        return render(request, 'station_gallery_photo_remove.html', {
            'station': station, 'img': photo, 'form': form
            })


class UserDetailsListView(ListView):
    model = User
    context_object_name = 'user_data'
    template_name = 'user_details.html'

    def get_queryset(self):
        try:
            queryset = User.objects.\
                get(username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("User does not exist!")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = \
            ExtAccessData.objects.order_by('-updated_at').filter(
                updated_by__username=self.kwargs.get('username'))[:25]
        return context


def custom_404(request):
    '''HTTP 404 custom handler
    '''
    return render_to_response('404.html')


def custom_500(request):
    '''HTTP 500 custom handler
    '''
    return render_to_response('500.html')


@user_passes_test(lambda u: u.is_superuser)
def refresh_fdsn(request):
    StationBookLogger(__name__).log_info(
        'Refreshing FDSN by {0}'.format(request.user))
    refresh_station_in_thread()
    return redirect('home')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('my_account')
        else:
            return render(request, 'my_account.html', {
                'user_form': user_form, 'profile_form': profile_form
                })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'my_account.html', {
            'user_form': user_form, 'profile_form': profile_form
            })