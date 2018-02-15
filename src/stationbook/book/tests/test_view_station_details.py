from django.test import TestCase
from django.urls import resolve, reverse

from ..models import FdsnNetwork, FdsnStation, ExtEntityBase, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, \
ExtBoreholeData, ExtBoreholeLayerData

class HomeTests(TestCase):
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

        url = reverse('station_details', kwargs={
            'network_code': self.network.code,
            'station_code': self.station.code
        })
        
        self.response = self.client.get(url)

    def test_station_details_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)