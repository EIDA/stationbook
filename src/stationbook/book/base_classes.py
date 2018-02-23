from django.views.generic import UpdateView
from django.utils import timezone
from django.http import Http404

from .models import FdsnNetwork, ExtAccessData
from .logger import StationBookLogger

class StationBookHelpers():
    @staticmethod
    def add_ext_access_data(user, station, desc):
        try:
            access = ExtAccessData()
            access.fdsn_station = station
            access.updated_by = user
            access.updated_at = timezone.now()
            access.description = desc
            access.save()
        except:
            StationBookLogger(__name__).log_exception(
                StationBookHelpers.__name__)


class StationUpdateViewBaseMixin(object):
    def __init__(self):
        pass
    
    def ensure_user_access_right(self):
        if not StationAccessManager.user_is_network_editor(
            user=self.request.user,
            network=FdsnNetwork.objects.get(
                code=self.kwargs.get('network_code'))):
                raise Http404("Write access to this network not granted!")


class StationUpdateViewBase(UpdateView, StationUpdateViewBaseMixin):
    def __init__(self, model, fields,
        template_name='station_edit.html',
        context_object_name='data'):
        self.model = model
        self.fields = fields
        self.template_name = template_name
        self.context_object_name = context_object_name


class StationAccessManager(object):
    def __init__(self):
        pass
    
    @staticmethod
    def user_is_network_editor(user, network):
        try:
            if not hasattr(user, 'profile'):
                return False
            elif user.profile in network.editors.all():
                return True
            else:
                return False
        except:
            StationBookLogger(__name__).log_exception(
                StationAccessManager.__name__)
            return False
    
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
            StationBookLogger(__name__).log_exception(
                StationAccessManager.__name__)
            return False