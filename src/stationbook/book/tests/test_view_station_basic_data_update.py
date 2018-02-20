from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import ExtBasicDataUpdateView

class StationBasicDataUpdateTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='station_edit_basic')

    # def test_station_basic_data_update_view_status_code(self):
    #     self.user_login()
    #     self.assertEquals(self.response.status_code, 200)

    # def test_station_basic_data_update_url_resolves_view(self):
    #     view = resolve('/networks/NET/station/STA/edit_basic/')
    #     self.assertEquals(view.func.view_class, ExtBasicDataUpdateView)