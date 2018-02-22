import tempfile

from django.test import TestCase
from django.test.client import Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..models import FdsnNetwork, FdsnStation, ExtEntityBase, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, \
ExtBoreholeData, ExtBoreholeLayerData, Photo

class NetworkStationTest(TestCase):
    def __init__(
        self, *args, 
        url, arguments={'network_code': 'NET', 'station_code': 'STA'}):

        TestCase.__init__(self, *args)
        self.url = url
        self.net_stat = arguments
        self.username = 'admin'
        self.password = 'password123'

    def setUp(self):
        User.objects.create_user(
            username=self.username,
            email='admin@example.com',
            password=self.password)
        
        self.network = FdsnNetwork.objects.create(code='NET')
        self.ebad = ExtBasicData.objects.create()
        self.eowd = ExtOwnerData.objects.create()
        self.emod = ExtMorphologyData.objects.create()
        self.ehod = ExtHousingData.objects.create()
        self.ebod = ExtBoreholeData.objects.create()
        self.ebodl = ExtBoreholeLayerData.objects.create(
            borehole_data=self.ebod, pk=1
        )

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
        
        # Create a temp image file for mocking purposes
        img = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.photo = Photo.objects.create(
            fdsn_station=self.station, pk=1, photo=img)
        
        self.user_login()
        url = reverse(self.url, kwargs=self.net_stat)
        self.response = self.client.get(url)

    def user_login(self):
        self.client.login(username=self.username, password=self.password)
    
    def user_logout(self):
        self.client.logout()