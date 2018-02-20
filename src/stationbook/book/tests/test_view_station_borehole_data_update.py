from django.urls import resolve, reverse

from .base_classes import NetworkStationTest

class StationBoreholeDataUpdateTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='station_edit_borehole')

    # def test_station_borehole_data_update_view_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)