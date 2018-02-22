from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import ExtMorphologyDataUpdateView

class StationMorphologyDataUpdateTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_edit_morphology')
    
    def test_station_morphology_data_update_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_station_morphology_data_update_url_resolves_view(self):
        view = resolve('/networks/NET/station/STA/edit_morphology')
        self.assertEquals(view.func.view_class, ExtMorphologyDataUpdateView)