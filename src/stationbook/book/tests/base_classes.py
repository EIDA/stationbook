import tempfile

from django.test import TestCase
from django.test.client import Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..models import (
    FdsnNode,
    FdsnNetwork,
    FdsnStation,
    ExtEntityBase,
    ExtBasicData,
    ExtOwnerData,
    ExtMorphologyData,
    ExtHousingData,
    ExtBoreholeData,
    ExtBoreholeLayerData,
    Photo,
)


class NetworkStationTest(TestCase):
    def __init__(
        self,
        *args,
        url,
        arguments={"network_code": "NET", "network_start_year": "1990"}
    ):

        TestCase.__init__(self, *args)
        self.url = url
        self.net_stat = arguments
        self.username = "admin"
        self.password = "password123"

    def setUp(self):
        User.objects.create_user(
            pk=1,
            username=self.username,
            email="admin@example.com",
            password=self.password,
        )

        self.node = FdsnNode.objects.create(
            pk=1, code="ODC", url_station="", url_routing=""
        )

        self.network = FdsnNetwork.objects.create(
            fdsn_node=self.node, pk=1, code="NET", start_date="1990-01-01 12:00"
        )
        self.ebad = ExtBasicData.objects.create()
        self.eowd = ExtOwnerData.objects.create()
        self.emod = ExtMorphologyData.objects.create()
        self.ehod = ExtHousingData.objects.create()
        self.ebod = ExtBoreholeData.objects.create()
        self.ebodl = ExtBoreholeLayerData.objects.create(borehole_data=self.ebod, pk=1)

        # Give newly creater user write access to the network
        self.network.editors.add(User.objects.get(pk=1).profile)

        self.station = FdsnStation.objects.create(
            pk=1,
            fdsn_network=self.network,
            code="STA",
            start_date="1980-01-01 12:00",
            creation_date="1990-01-01 12:00",
            latitude=50,
            longitude=100,
            elevation=600,
            ext_basic_data=self.ebad,
            ext_owner_data=self.eowd,
            ext_morphology_data=self.emod,
            ext_housing_data=self.ehod,
            ext_borehole_data=self.ebod,
        )

        # Create a temp image file for mocking purposes
        img = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.photo = Photo.objects.create(fdsn_station=self.station, pk=1, photo=img)

        url = reverse(self.url, kwargs=self.net_stat)
        self.response = self.client.get(url)

    def user_login(self):
        self.client.login(username=self.username, password=self.password)

    def user_logout(self):
        self.client.logout()

    def login_and_refresh(self):
        self.user_login()
        url = reverse(self.url, kwargs=self.net_stat)
        self.response = self.client.get(url)

    def logout_and_refresh(self):
        self.user_logout()
        url = reverse(self.url, kwargs=self.net_stat)
        self.response = self.client.get(url)
