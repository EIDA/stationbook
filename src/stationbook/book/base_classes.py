from django.views.generic import UpdateView
from django.utils import timezone
from django.http import Http404
from django.db.models import Q, Count
from django.core.cache import cache
from django.forms.models import model_to_dict

from .models import FdsnNetwork, FdsnStation, ExtAccessData
from .logger import StationBookLoggerMixin

class StationBookHelpers(StationBookLoggerMixin):
    @staticmethod
    def add_ext_access_data(user, station, desc):
        try:
            access = ExtAccessData()
            access.ext_network_code = station.fdsn_network.code
            access.ext_network_start_year = station.fdsn_network.get_start_year()
            access.ext_station_code = station.code
            access.ext_station_start_year = station.get_start_year()
            access.fdsn_station = station
            access.updated_by = user
            access.updated_at = timezone.now()
            access.description = desc
            access.save()
        except:
            raise

    @staticmethod
    def get_stations():
        try:
            if not cache.get('stations'):
                result = []
                stations = FdsnStation.objects.select_related('fdsn_network')

                for s in stations:
                    result.append({
                        'network_pk': s.fdsn_network.pk,
                        'station_pk': s.pk,
                        'network_code': s.fdsn_network.code,
                        'network_code_year': s.fdsn_network.get_code_year,
                        'network_start_year': s.fdsn_network.start_date.year,
                        'code': s.code,
                        'site_name': s.site_name,
                        'start_date': s.get_start_date,
                        'start_year': s.get_start_year,
                        'latitude': s.latitude,
                        'longitude': s.longitude,
                        'is_open': s.is_open
                    })
                cache.set('stations', result, 86400)
            return cache.get('stations')
        except:
            raise

    @staticmethod
    def get_networks_by_year():
        try:
            if not cache.get('networks_by_year'):
                result = set()
                # Get only networks having stations
                networks = FdsnNetwork.objects.annotate(
                    c=Count("fdsn_stations")
                ).filter(c__gt=0)
                
                for n in networks:
                    result.add(
                        (
                            n.code,
                            n.start_date.year,
                            n.restricted_status
                        )
                    )
                cache.set('networks_by_year', result, 86400)
            return cache.get('networks_by_year')
        except:
            raise


class StationUpdateViewBaseMixin(object):
    def __init__(self):
        pass
    
    def ensure_user_access_right(self):
        if not StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network_code=self.kwargs.get('network_code'),
            network_start_year=self.kwargs.get('network_start_year')):
            raise Http404("Write access to this network not granted!")


class StationUpdateViewBase(UpdateView, StationUpdateViewBaseMixin):
    def __init__(self, model, fields,
        template_name='station_edit.html',
        context_object_name='data'):
        self.model = model
        self.fields = fields
        self.template_name = template_name
        self.context_object_name = context_object_name


class StationAccessManager(StationBookLoggerMixin):
    def __init__(self):
        pass
    
    @staticmethod
    def user_is_network_editor(user, network_code, network_start_year):
        try:
            if not hasattr(user, 'profile'):
                return False
            else:
                for n in user.profile.fdsn_networks.all():
                    if n.code == network_code and n.get_start_year() == network_start_year:
                        return True
                return False
        except:
            raise
    
    @staticmethod
    def user_is_station_editor(user, station):
        try:
            if not hasattr(user, 'profile'):
                return False
            elif user.profile in station.fdsn_network.editors.all():
                return True
            else:
                return False
        except:
            raise
