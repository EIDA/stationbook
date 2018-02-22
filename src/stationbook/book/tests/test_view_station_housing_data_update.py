from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import ExtHousingDataUpdateView

class StationHousingDataUpdateTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_edit_housing')

    def test_station_housing_data_update_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_station_housing_data_update_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 302)

    def test_station_housing_data_update_url_resolves_view(self):
        view = resolve('/networks/NET/station/STA/edit_housing')
        self.assertEquals(view.func.view_class, ExtHousingDataUpdateView)