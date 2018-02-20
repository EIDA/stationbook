from django.urls import resolve, reverse

from .base_classes import NetworkStationTest

class HomeTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='station_details')

    # def test_station_details_view_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)