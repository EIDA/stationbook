# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
from functools import reduce

from django.http import Http404
from django.shortcuts import \
    get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.db.models import Q, Count

from .fdsn.fdsn_manager import FdsnManager, FdsnStationChannelsManager
from .models import \
    FdsnNode, FdsnNetwork, FdsnStation, ExtBasicData, ExtOwnerData, \
    ExtMorphologyData, ExtHousingData, ExtAccessData, ExtBoreholeData, \
    ExtBoreholeLayerData, Photo, Link, SearchFdsnStationModel

from .base_classes import \
    StationBookHelpers, StationUpdateViewBase, StationAccessManager

from .fdsn.base_classes import NodeWrapper

from .helpers.doi_helper import DOIHelper

from .forms import \
    UserForm, ProfileForm, AddBoreholeLayerForm, EditBoreholeLayerForm, \
    RemoveBoreholeLayerForm, StationPhotoForm, StationPhotoEditForm, \
    StationPhotoRemoveForm, SearchAdvancedForm


# Stations list view is used as a home screen for the Station Book
class HomeListView(ListView):
    model = FdsnStation
    context_object_name = 'stations'
    template_name = 'home.html'

    def get_queryset(self):
        queryset = StationBookHelpers.get_stations()
        return queryset


class SearchListView(ListView):
    model = FdsnStation
    context_object_name = 'data'
    template_name = 'search_results.html'

    def get_queryset(self):
        if self._get_search_phrase() is None:
            queryset = None
        else:
            queryset = FdsnStation.objects.all()

        query = self.request.GET.get('search_text')
        if query:
            query_list = query.split()
            queryset = queryset.filter(
                reduce(operator.and_, (
                    Q(code__icontains=q) for q in query_list)) |
                reduce(operator.and_, (
                    Q(site_name__icontains=q) for q in query_list)))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_phrase'] = self._get_search_phrase()
        return context

    def _get_search_phrase(self):
        return (
            (lambda x: x if len(x) > 0 else None)(
                self.request.GET.get('search_text', '')
            )
        )


class NodesListView(ListView):
    model = FdsnNode
    context_object_name = 'data'
    template_name = 'nodes.html'

    def get_queryset(self):
        queryset = FdsnNode.objects.all().order_by('code')
        return queryset


class NodeDetailsListView(ListView):
    model = FdsnNode
    context_object_name = 'node'
    template_name = 'node_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnNode.objects.get(pk=self.kwargs.get('node_pk'))
        except FdsnNode.DoesNotExist:
            raise Http404("Node does not exist!")
        return queryset


class NetworksListView(ListView):
    model = None
    context_object_name = 'data'
    template_name = 'networks.html'

    def get_queryset(self):
        queryset = StationBookHelpers.get_networks_by_year()
        return queryset


class RecentChangesListView(ListView):
    model = ExtAccessData
    context_object_name = 'data'
    template_name = 'recent_changes.html'

    def get_queryset(self):
        queryset = ExtAccessData.objects.order_by('-updated_at')[:1000]
        return queryset


class LinksListView(ListView):
    model = Link
    context_object_name = 'links'
    template_name = 'links.html'

    def get_queryset(self):
        queryset = Link.objects.order_by('category')
        return queryset


class AboutListView(ListView):
    model = None
    context_object_name = 'data'
    template_name = 'about.html'

    def get_queryset(self):
        return None


class NetworkDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'network'
    template_name = 'network_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnNetwork.objects.filter(
                code=self.kwargs.get('network_code'),
                start_date__year=self.kwargs.get('network_start_year')
            )[:1].get()
        except FdsnNetwork.DoesNotExist:
            raise Http404("Network does not exist!")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stations'] = FdsnStation.objects.filter(
            fdsn_network__code=self.kwargs.get('network_code'),
            fdsn_network__start_date__year=self.kwargs.get('network_start_year')
        )

        context['network_doi'] = self.get_network_doi(
            self.kwargs.get('network_code'),
            self.kwargs.get('network_start_year')
        )

        return context

    def get_network_doi(self, network_code, network_start_year):
        dh = DOIHelper()
        doi = dh.get_network_doi(network_code, network_start_year)
        return doi


class StationDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_details.html'
    station = None

    def get_queryset(self):
        try:
            self.station = FdsnStation.objects.get(
                fdsn_network__code=self.kwargs.get('network_code'),
                fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
                code=self.kwargs.get('station_code'),
                start_date__year=self.kwargs.get('station_start_year')
            )
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return self.station

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        node_wrapper = NodeWrapper(self.station.fdsn_network.fdsn_node)
        channel_url = node_wrapper.build_url_station_channel_level().format(
            self.station.fdsn_network.code,
            self.station.code
        )
        context['fdsn_station_link'] = channel_url

        fdsn_cha_manager = FdsnStationChannelsManager()
        scg = fdsn_cha_manager.discover_station_channels(
            network_pk=self.station.fdsn_network.pk,
            station_pk=self.station.pk)
        context['station_channels'] = scg.channels

        user_is_network_editor = StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network_code=self.station.fdsn_network.code,
            network_start_year=self.station.fdsn_network.get_start_year()
        )
        context['user_is_network_editor'] = user_is_network_editor
        return context


class StationGalleryListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_gallery.html'

    def get_queryset(self):
        try:
            queryset = FdsnStation.objects.get(
                fdsn_network__code=self.kwargs.get('network_code'),
                fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
                code=self.kwargs.get('station_code'),
                start_date__year=self.kwargs.get('station_start_year')
            )
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_is_network_editor = StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network_code=self.kwargs.get('network_code'),
            network_start_year=self.kwargs.get('network_start_year')
        )
        context['user_is_network_editor'] = user_is_network_editor
        return context


@method_decorator(login_required, name='dispatch')
class ExtBasicDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(
            self,
            model=ExtBasicData,
            fields=('description', 'start', 'end', )
        )

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(
            self.model,
            station__fdsn_network__code=self.kwargs.get('network_code'),
            station__fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
            station__code=self.kwargs.get('station_code'),
            station__start_date__year=self.kwargs.get('station_start_year')
        )
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        print(data.station)

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated basic data')

        return redirect(
            'station_details',
            network_code=data.station.fdsn_network.code,
            network_start_year=data.station.fdsn_network.get_start_year(),
            station_code=data.station.code,
            station_start_year=data.station.get_start_year()
        )


@method_decorator(login_required, name='dispatch')
class ExtOwnerDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(
            self,
            model=ExtOwnerData,
            fields=(
                'name_first', 'name_last', 'department', 'agency', 'city',
                'street', 'country', 'phone', 'email',
            )
        )

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(
            self.model,
            station__fdsn_network__code=self.kwargs.get('network_code'),
            station__fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
            station__code=self.kwargs.get('station_code'),
            station__start_date__year=self.kwargs.get('station_start_year')
        )
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated owner data')

        return redirect(
            'station_details',
            network_code=data.station.fdsn_network.code,
            network_start_year=data.station.fdsn_network.get_start_year(),
            station_code=data.station.code,
            station_start_year=data.station.get_start_year()
        )


@method_decorator(login_required, name='dispatch')
class ExtMorphologyDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(
            self,
            model=ExtMorphologyData,
            fields=(
                'description', 'geological_unit', 'morphology_class',
                'ground_type_ec8', 'groundwater_depth', 'vs_30', 'f0',
                'amp_f0', 'basin_flag', 'bedrock_depth',
            )
        )

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(
            self.model,
            station__fdsn_network__code=self.kwargs.get('network_code'),
            station__fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
            station__code=self.kwargs.get('station_code'),
            station__start_date__year=self.kwargs.get('station_start_year')
        )
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated morphology data')

        return redirect(
            'station_details',
            network_code=data.station.fdsn_network.code,
            network_start_year=data.station.fdsn_network.get_start_year(),
            station_code=data.station.code,
            station_start_year=data.station.get_start_year()
        )


@method_decorator(login_required, name='dispatch')
class ExtHousingDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(
            self,
            model=ExtHousingData,
            fields=(
                'description', 'housing_class', 'in_building',
                'numer_of_storeys', 'distance_to_building',
            )
        )

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(
            self.model,
            station__fdsn_network__code=self.kwargs.get('network_code'),
            station__fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
            station__code=self.kwargs.get('station_code'),
            station__start_date__year=self.kwargs.get('station_start_year')
        )
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated housing data')

        return redirect(
            'station_details',
            network_code=data.station.fdsn_network.code,
            network_start_year=data.station.fdsn_network.get_start_year(),
            station_code=data.station.code,
            station_start_year=data.station.get_start_year()
        )


@method_decorator(login_required, name='dispatch')
class ExtBoreholeDataUpdateView(StationUpdateViewBase):
    def __init__(self):
        StationUpdateViewBase.__init__(
            self,
            model=ExtBoreholeData,
            fields=('depth', )
        )

    def get_object(self):
        self.ensure_user_access_right()
        obj = get_object_or_404(
            self.model,
            station__fdsn_network__code=self.kwargs.get('network_code'),
            station__fdsn_network__start_date__year=self.kwargs.get('network_start_year'),
            station__code=self.kwargs.get('station_code'),
            station__start_date__year=self.kwargs.get('station_start_year')
        )
        return obj

    @transaction.atomic
    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        StationBookHelpers.add_ext_access_data(
            self.request.user, data.station, 'Updated borehole data')

        return redirect(
            'station_details',
            network_code=data.station.fdsn_network.code,
            network_start_year=data.station.fdsn_network.get_start_year(),
            station_code=data.station.code,
            station_start_year=data.station.get_start_year()
        )


@login_required
@transaction.atomic
def station_borehole_layer_add(request, network_code, network_start_year, station_code, station_start_year):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year)

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

            return redirect(
                'station_details',
                network_code=station.fdsn_network.code,
                network_start_year=station.fdsn_network.get_start_year(),
                station_code=station.code,
                station_start_year=station.get_start_year()
            )
    else:
        form = AddBoreholeLayerForm()
        return render(
            request, 'station_borehole_layer_add.html',
            {'station': station, 'form': form})


@login_required
@transaction.atomic
def station_borehole_layer_edit(request, network_code, network_start_year, station_code, station_start_year, layer_pk):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year)
    borehole_layer = get_object_or_404(ExtBoreholeLayerData, pk=layer_pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = EditBoreholeLayerForm(request.POST, instance=borehole_layer)
        form.save()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Edited borehole layer ({0})'.format(
                borehole_layer.description))

        return redirect(
            'station_details',
            network_code=station.fdsn_network.code,
            network_start_year=station.fdsn_network.get_start_year(),
            station_code=station.code,
            station_start_year=station.get_start_year()
        )
    else:
        form = EditBoreholeLayerForm(instance=borehole_layer)
        return render(
            request, 'station_borehole_layer_edit.html',
            {'station': station, 'layer': borehole_layer, 'form': form})


@login_required
@transaction.atomic
def station_borehole_layer_remove(request, network_code, network_start_year, station_code, station_start_year, layer_pk):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year)
    borehole_layer = get_object_or_404(
        ExtBoreholeLayerData, pk=layer_pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = RemoveBoreholeLayerForm(request.POST)
        ExtBoreholeLayerData.objects.get(pk=layer_pk).delete()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Removed borehole layer ({0})'.format(
                borehole_layer.description))

        return redirect(
            'station_details',
            network_code=station.fdsn_network.code,
            network_start_year=station.fdsn_network.get_start_year(),
            station_code=station.code,
            station_start_year=station.get_start_year()
        )
    else:
        form = RemoveBoreholeLayerForm()
        return render(
            request, 'station_borehole_layer_remove.html', {
                'station': station,
                'layer': borehole_layer,
                'form': form
                })


@login_required
@transaction.atomic
def station_photo_upload(request, network_code, network_start_year, station_code, station_start_year):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            station = FdsnStation.objects.get(
                fdsn_network__code=network_code,
                fdsn_network__start_date__year=network_start_year,
                code=station_code,
                start_date__year=station_start_year
            )

            photo = form.save(commit=False)
            photo.fdsn_station = station
            photo.ext_network_code = network_code
            photo.ext_network_start_year = network_start_year
            photo.ext_station_code = station.code
            photo.ext_station_start_year = station.get_start_year()
            photo.save()

            StationBookHelpers.add_ext_access_data(
                request.user, station,
                'Added photo ({0})'.format(photo.description))

            return redirect(
                'station_gallery',
                network_code=network_code,
                network_start_year=network_start_year,
                station_code=station_code,
                station_start_year=station_start_year
            )
    else:
        form = StationPhotoForm()
        return render(request, 'upload_photo.html', {
            'station': station, 'form': form})


@login_required
@transaction.atomic
def station_photo_edit(request, network_code, network_start_year, station_code, station_start_year, photo_pk):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year
        )
    photo = get_object_or_404(Photo, pk=photo_pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoEditForm(request.POST, instance=photo)
        form.save()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Photo edited ({0})'.format(
                photo.description))

        return redirect(
            'station_gallery',
            network_code=network_code,
            network_start_year=network_start_year,
            station_code=station_code,
            station_start_year=station_start_year
        )
    else:
        form = StationPhotoEditForm(instance=photo)
        return render(request, 'station_gallery_photo_edit.html', {
            'station': station, 'img': photo, 'form': form
            })


@login_required
@transaction.atomic
def station_photo_remove(request, network_code, network_start_year, station_code, station_start_year, photo_pk):
    station = get_object_or_404(
        FdsnStation,
        fdsn_network__code=network_code,
        fdsn_network__start_date__year=network_start_year,
        code=station_code,
        start_date__year=station_start_year)
    photo = get_object_or_404(Photo, pk=photo_pk)

    if not StationAccessManager.user_is_station_editor(request.user, station):
        raise Http404("Write access to this network not granted!")

    if request.method == 'POST':
        form = StationPhotoRemoveForm(request.POST, instance=photo)
        Photo.objects.get(pk=photo_pk).delete()

        StationBookHelpers.add_ext_access_data(
            request.user, station,
            'Removed photo ({0})'.format(
                photo.description))

        return redirect(
            'station_gallery',
            network_code=network_code,
            network_start_year=network_start_year,
            station_code=station_code,
            station_start_year=station_start_year
        )
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
                updated_by__username=self.kwargs.get('username')
            )[:25]
        return context


def search_advanced_networks(request):
    pass


def search_advanced(request):
    if request.method == 'POST':
        form = SearchAdvancedForm(request.POST)
        if form.is_valid():
            net_code = form.cleaned_data['network_code'].upper()
            network_class = form.cleaned_data['network_class']
            network_access = form.cleaned_data['network_access']
            stat_code = form.cleaned_data['station_code'].upper()
            station_status = form.cleaned_data['station_status']
            station_access = form.cleaned_data['station_access']
            site_name = form.cleaned_data['site_name']
            latitude_min = form.cleaned_data['latitude_min']
            latitude_max = form.cleaned_data['latitude_max']
            longitude_min = form.cleaned_data['longitude_min']
            longitude_max = form.cleaned_data['longitude_max']
            start_year_from = form.cleaned_data['start_year_from']
            start_year_to = form.cleaned_data['start_year_to']
            end_year_from = form.cleaned_data['end_year_from']
            end_year_to = form.cleaned_data['end_year_to']
            geological_unit = form.cleaned_data['geological_unit']
            morphology_class = form.cleaned_data['morphology_class']
            ground_type_ec8 = form.cleaned_data['ground_type_ec8']
            basin_flag = form.cleaned_data['basin_flag']
            vs30_from = form.cleaned_data['vs30_from']
            vs30_to = form.cleaned_data['vs30_to']
            f0_from = form.cleaned_data['f0_from']
            f0_to = form.cleaned_data['f0_to']

            data = FdsnStation.objects.all()
            search_phrase = ''

            if net_code:
                data = data.filter(
                    fdsn_network__code__icontains=net_code
                )
                search_phrase += 'Network: {}, '.format(
                    net_code
                )

            if (network_class and network_class == 'permanent'):
                data = data.filter(
                    fdsn_network__code__regex=r'[A-Z]{2}'
                )
                search_phrase += 'Network class: {}, '.format(
                    network_class
                )

            if (network_class and network_class == 'temporary'):
                data = data.filter(
                    fdsn_network__code__regex=r'\d[A-Z]{1}'
                )
                search_phrase += 'Network class: {}, '.format(
                    network_class
                )

            if (network_access and network_access == 'restricted'):
                data = data.filter(
                    fdsn_network__restricted_status='closed'
                )
                search_phrase += 'Network access: {}, '.format(
                    network_access
                )

            if (network_access and network_access == 'unrestricted'):
                data = data.filter(
                    fdsn_network__restricted_status='open'
                )
                search_phrase += 'Network access: {}, '.format(
                    network_access
                )

            if stat_code:
                data = data.filter(
                    code__icontains=stat_code
                )
                search_phrase += 'Station: {}, '.format(
                    stat_code
                )

            if (station_status and station_status == 'open'):
                data = data.filter(
                    end_date__isnull=True
                )
                search_phrase += 'Station status: {}, '.format(
                    station_status
                )

            if (station_status and station_status == 'closed'):
                data = data.filter(
                    end_date__isnull=False
                )
                search_phrase += 'Station status: {}, '.format(
                    station_status
                )

            if (station_access and station_access == 'restricted'):
                data = data.filter(
                    restricted_status='closed'
                )
                search_phrase += 'Station access: {}, '.format(
                    network_access
                )

            if (station_access and station_access == 'unrestricted'):
                data = data.filter(
                    restricted_status='open'
                )
                search_phrase += 'Station access: {}, '.format(
                    network_access
                )

            if site_name:
                data = data.filter(
                    site_name__icontains=site_name
                )
                search_phrase += 'Site: {}, '.format(
                    site_name
                )

            if latitude_min:
                data = data.filter(
                    latitude__gte=latitude_min
                )
                search_phrase += 'Lat min: {}, '.format(
                    latitude_min
                )

            if latitude_max:
                data = data.filter(
                    latitude__lte=latitude_max
                )
                search_phrase += 'Lat max: {}, '.format(
                    latitude_max
                )

            if longitude_min:
                data = data.filter(
                    longitude__gte=longitude_min
                )
                search_phrase += 'Lon min: {}, '.format(
                    longitude_min
                )

            if longitude_max:
                data = data.filter(
                    longitude__lte=longitude_max
                )
                search_phrase += 'Lon max: {}, '.format(
                    longitude_max
                )

            if start_year_from:
                data = data.filter(
                    start_date__year__gte=start_year_from
                )
                search_phrase += 'Start from: {}, '.format(
                    start_year_from
                )

            if start_year_to:
                data = data.filter(
                    start_date__year__lte=start_year_to
                )
                search_phrase += 'Start to: {}, '.format(
                    start_year_to
                )

            if end_year_from:
                data = data.filter(
                    end_date__year__gte=end_year_from
                )
                search_phrase += 'End from: {}, '.format(
                    end_year_from
                )

            if end_year_to:
                data = data.filter(
                    end_date__year__lte=end_year_to
                )
                search_phrase += 'End to: {}, '.format(
                    end_year_to
                )

            if geological_unit:
                data = data.filter(
                    ext_morphology_data__geological_unit=geological_unit
                )
                search_phrase += 'Geological unit: {}, '.format(
                    geological_unit
                )

            if morphology_class:
                data = data.filter(
                    ext_morphology_data__morphology_class=morphology_class
                )
                search_phrase += 'Morphology class: {}, '.format(
                    morphology_class
                )

            if ground_type_ec8:
                data = data.filter(
                    ext_morphology_data__ground_type_ec8=ground_type_ec8
                )
                search_phrase += 'Ground type EC8: {}, '.format(
                    ground_type_ec8
                )

            if basin_flag:
                data = data.filter(
                    ext_morphology_data__basin_flag=basin_flag
                )
                search_phrase += 'Basin flag: {}, '.format(
                    basin_flag
                )

            if vs30_from:
                data = data.filter(
                    ext_morphology_data__vs_30__gte=vs30_from
                )
                search_phrase += 'Vs 30 min: {}, '.format(
                    vs30_from
                )

            if vs30_to:
                data = data.filter(
                    ext_morphology_data__vs_30__lte=vs30_to
                )
                search_phrase += 'Vs 30 max: {}, '.format(
                    vs30_to
                )

            if f0_from:
                data = data.filter(
                    ext_morphology_data__f0__gte=f0_from
                )
                search_phrase += 'f0 min: {}, '.format(
                    f0_from
                )

            if f0_to:
                data = data.filter(
                    ext_morphology_data__f0__lte=f0_to
                )
                search_phrase += 'f0 max: {}, '.format(
                    f0_to
                )

            return render(
                request,
                'search_results.html',
                {
                    'data': data,
                    'search_phrase': search_phrase
                }
            )
        else:
            return render(
                request,
                'search_advanced.html',
                {
                    'form': form
                }
            )
    else:
        form = SearchAdvancedForm(instance=SearchFdsnStationModel())
        return render(
            request,
            'search_advanced.html',
            {
                'form': form
            }
        )


def custom_404(request, exception=None):
    '''HTTP 404 custom handler
    '''
    return render(request, '404.html', {'exception': exception})


def custom_500(request, exception=None):
    '''HTTP 500 custom handler
    '''
    return render(request, '500.html', {'exception': exception})


@user_passes_test(lambda u: u.is_superuser)
def refresh_fdsn(request):
    fdsn_net_manager = FdsnManager()
    fdsn_net_manager.process_fdsn_in_thread()
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
            'user_profile': request.user.profile,
            'user_form': user_form,
            'profile_form': profile_form
            })
