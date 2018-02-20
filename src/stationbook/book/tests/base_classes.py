from django.test import TestCase
from django.urls import resolve, reverse

from ..models import FdsnNetwork, FdsnStation, ExtEntityBase, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, \
ExtBoreholeData, ExtBoreholeLayerData

class NetworkStationTest(TestCase):
    def __init__(
        self, *args, 
        url, arguments={'network_code': 'NET', 'station_code': 'STA'}):

        TestCase.__init__(self, *args)
        self.url = url
        self.net_stat = arguments

    def setUp(self):
        self.network = FdsnNetwork.objects.create(code='NET')
        self.ebad = ExtBasicData.objects.create()
        self.eowd = ExtOwnerData.objects.create()
        self.emod = ExtMorphologyData.objects.create()
        self.ehod = ExtHousingData.objects.create()
        self.ebod = ExtBoreholeData.objects.create()
        self.station = FdsnStation.objects.create(
            fdsn_network=self.network,
            code='STA',
            latitude=50,
            longitude=100,
            elevation=600,
            ext_basic_data=self.ebad,
            ext_owner_data=self.eowd,
            ext_morphology_data=self.emod,
            ext_housing_data=self.ehod,
            ext_borehole_data=self.ebod)

        url = reverse(self.url, kwargs=self.net_stat)
        self.response = self.client.get(url)