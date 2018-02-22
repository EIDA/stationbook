from django.views.generic import UpdateView
from django.utils import timezone

from .models import ExtAccessData
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
                add_ext_access_data.__name__)

    @staticmethod
    def user_is_network_editor(user, network):
        try:
            if user.profile in network.eitors.all():
                return True
            else:
                return False
        except:
            return False
    
    @staticmethod
    def user_is_station_editor(user, station):
        try:
            if user.profile in station.fdsn_network.eitors.all():
                return True
            else:
                return False
        except:
            return False

class StationUpdateViewBase(UpdateView):
    def __init__(self, model, fields,
        template_name='station_edit.html',
        context_object_name='data'):
        self.model = model
        self.fields = fields
        self.template_name = template_name
        self.context_object_name = context_object_name