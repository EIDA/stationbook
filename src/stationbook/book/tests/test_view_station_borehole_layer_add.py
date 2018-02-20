from django.urls import resolve, reverse

from .base_classes import NetworkStationTest

class StationBoreholeLayerAddTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='station_add_borehole_layer')

    # def test_station_borehole_layer_add_view_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)