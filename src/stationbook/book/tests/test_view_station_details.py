from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import StationDetailsListView

class HomeTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self,
            *args,
            url='station_details',
            arguments={
                'network_pk': '1',
                'station_pk': '1'
            }
        )

    def test_station_details_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_station_details_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_station_details_url_resolves_view(self):
        view = resolve('/networks/1/station/1/')
        self.assertEquals(view.func.view_class, StationDetailsListView)