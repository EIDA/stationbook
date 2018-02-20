from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..models import FdsnNetwork, FdsnStation, ExtEntityBase, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, \
ExtBoreholeData, ExtBoreholeLayerData

class HomeTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_details')

    def test_station_details_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)