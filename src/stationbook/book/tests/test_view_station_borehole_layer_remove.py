from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import station_borehole_layer_remove

class StationBoreholeLayerRemoveTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self, *args,
            url='station_remove_borehole_layer',
            arguments={'network_code': 'NET', 'station_code': 'STA', 'pk': '1' })

    def test_station_borehole_layer_remove_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_station_borehole_layer_remove_url_resolves_view(self):
        view = resolve('/networks/NET/station/STA/remove_borehole_layer/1')
        self.assertEquals(view.func, station_borehole_layer_remove)