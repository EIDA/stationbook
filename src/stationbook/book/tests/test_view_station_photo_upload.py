from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import station_photo_upload

class StationPhotoUploadTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_photo_upload')

    def test_station_photo_upload_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_station_photo_upload_url_resolves_view(self):
        view = resolve('/networks/NET/station/STA/upload_photo')
        self.assertEquals(view.func, station_photo_upload)