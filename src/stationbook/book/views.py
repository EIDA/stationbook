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
from django.db.models import Q, Count

from .fdsn.fdsn_manager import FdsnManager, FdsnStationChannelsManager
from .models import \
    FdsnNode, FdsnNetwork, FdsnStation, ExtBasicData, ExtOwnerData, \
    ExtMorphologyData, ExtHousingData, ExtAccessData, ExtBoreholeData, \
    ExtBoreholeLayerData, Photo, Link, SearchFdsnStationModel

from .base_classes import \
    StationBookHelpers, StationUpdateViewBase, StationAccessManager

from .fdsn.base_classes import NodeWrapper

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
        queryset = FdsnStation.objects.order_by('?')[:1]
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
    model = FdsnNetwork
    context_object_name = 'data'
    template_name = 'networks.html'

    def get_queryset(self):
        queryset = FdsnNetwork.objects.annotate(
            num_stations=Count('fdsn_stations')).filter(
                num_stations__gt=0).order_by('code')
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


class NetworkDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'network'
    template_name = 'network_details.html'

    def get_queryset(self):
        try:
            queryset = FdsnNetwork.objects.get(
                pk=self.kwargs.get('network_pk')
            )
        except FdsnNetwork.DoesNotExist:
            raise Http404("Network does not exist!")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stations'] = FdsnStation.objects.filter(
            fdsn_network__pk=self.kwargs.get('network_pk'))
        return context


class StationDetailsListView(ListView):
    model = FdsnStation
    context_object_name = 'station'
    template_name = 'station_details.html'
    station = None

    def get_queryset(self):
        try:
            self.station = FdsnStation.objects.get(
                pk=self.kwargs.get('station_pk'))
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
            network=self.station.fdsn_network
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
                fdsn_network__pk=self.kwargs['network_pk'],
                pk=self.kwargs.get('station_pk')
            )
        except FdsnStation.DoesNotExist:
            raise Http404("Station does not exist!")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_is_network_editor = StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network=FdsnNetwork.objects.get(
                pk=self.kwargs.get('network_pk')
            )
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
            station__fdsn_network__pk=self.kwargs['network_pk'],
            station__pk=self.kwargs['station_pk']
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
            network_pk=data.station.fdsn_network.pk,
            station_pk=data.station.pk
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
            station__fdsn_network__pk=self.kwargs['network_pk'],
            station__pk=self.kwargs['station_pk']
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
            network_pk=data.station.fdsn_network.pk,
            station_pk=data.station.pk
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
            station__fdsn_network__pk=self.kwargs['network_pk'],
            station__pk=self.kwargs['station_pk']
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
            network_pk=data.station.fdsn_network.pk,
            station_pk=data.station.pk
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
            station__fdsn_network__pk=self.kwargs['network_pk'],
            station__pk=self.kwargs['station_pk']
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
            network_pk=data.station.fdsn_network.pk,
            station_pk=data.station.pk
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
            station__fdsn_network__pk=self.kwargs['network_pk'],
            station__pk=self.kwargs['station_pk']
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
            network_pk=data.station.fdsn_network.pk,
            station_pk=data.station.pk
        )


@login_required
@transaction.atomic
def station_borehole_layer_add(request, network_pk, station_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)

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
                network_pk=network_pk,
                station_pk=station_pk
            )
    else:
        form = AddBoreholeLayerForm()
        return render(
            request, 'station_borehole_layer_add.html',
            {'station': station, 'form': form})


@login_required
@transaction.atomic
def station_borehole_layer_edit(request, network_pk, station_pk, layer_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)
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
            network_pk=network_pk,
            station_pk=station_pk
        )
    else:
        form = EditBoreholeLayerForm(instance=borehole_layer)
        return render(
            request, 'station_borehole_layer_edit.html',
            {'station': station, 'layer': borehole_layer, 'form': form})


@login_required
@transaction.atomic
def station_borehole_layer_remove(request, network_pk, station_pk, layer_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)
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
            network_pk=network_pk,
            station_pk=station_pk
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
def station_photo_upload(request, network_pk, station_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)

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

            return redirect(
                'station_gallery',
                network_pk=network_pk,
                station_pk=station_pk
            )
    else:
        form = StationPhotoForm()
        return render(request, 'upload_photo.html', {
            'station': station, 'form': form})


@login_required
@transaction.atomic
def station_photo_edit(request, network_pk, station_pk, photo_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)
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
            network_pk=network_pk,
            station_pk=station_pk
        )
    else:
        form = StationPhotoEditForm(instance=photo)
        return render(request, 'station_gallery_photo_edit.html', {
            'station': station, 'img': photo, 'form': form
            })


@login_required
@transaction.atomic
def station_photo_remove(request, network_pk, station_pk, photo_pk):
    station = get_object_or_404(
        FdsnStation, fdsn_network__pk=network_pk, pk=station_pk)
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
            network_pk=network_pk,
            station_pk=station_pk
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


def search_advanced(request):
    if request.method == 'POST':
        form = SearchAdvancedForm(request.POST)
        if form.is_valid():
            net_code = form.cleaned_data['network_code'].upper()
            stat_code = form.cleaned_data['station_code'].upper()
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

            data = FdsnStation.objects.all()
            search_phrase = ''

            if net_code:
                data = data.filter(fdsn_network__code__icontains=net_code)
                search_phrase += 'Network: {}, '.format(net_code)

            if stat_code:
                data = data.filter(code__icontains=stat_code)
                search_phrase += 'Station: {}, '.format(stat_code)

            if site_name:
                data = data.filter(site_name__icontains=site_name)
                search_phrase += 'Site: {}, '.format(site_name)

            if latitude_min:
                data = data.filter(latitude__gte=latitude_min)
                search_phrase += 'Lat min: {}, '.format(latitude_min)

            if latitude_max:
                data = data.filter(latitude__lte=latitude_max)
                search_phrase += 'Lat max: {}, '.format(latitude_max)

            if longitude_min:
                data = data.filter(longitude__gte=longitude_min)
                search_phrase += 'Lon min: {}, '.format(longitude_min)

            if longitude_max:
                data = data.filter(longitude__lte=longitude_max)
                search_phrase += 'Lon max: {}, '.format(longitude_max)

            if start_year_from:
                data = data.filter(start_date__year__gte=start_year_from)
                search_phrase += 'Start from: {}, '.format(start_year_from)

            if start_year_to:
                data = data.filter(start_date__year__lte=start_year_to)
                search_phrase += 'Start to: {}, '.format(start_year_to)

            if end_year_from:
                data = data.filter(end_date__year__gte=end_year_from)
                search_phrase += 'End from: {}, '.format(end_year_from)

            if end_year_to:
                data = data.filter(end_date__year__lte=end_year_to)
                search_phrase += 'End to: {}, '.format(end_year_to)

            if geological_unit:
                data = data.filter(ext_morphology_data__geological_unit=geological_unit)
                search_phrase += 'Geological unit: {}, '.format(geological_unit)

            if morphology_class:
                data = data.filter(ext_morphology_data__morphology_class=morphology_class)
                search_phrase += 'Morphology class: {}, '.format(morphology_class)

            if ground_type_ec8:
                data = data.filter(ext_morphology_data__ground_type_ec8=ground_type_ec8)
                search_phrase += 'Ground type EC8: {}, '.format(ground_type_ec8)

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
    return render_to_response('404.html', {'exception': exception})


def custom_500(request, exception=None):
    '''HTTP 500 custom handler
    '''
    return render_to_response('500.html', {'exception': exception})


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
