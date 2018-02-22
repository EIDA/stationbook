from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import StationGalleryListView

class StationGalleryTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_gallery')

    def test_station_gallery_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_station_gallery_url_resolves_view(self):
        view = resolve('/networks/NET/station/STA/gallery')
        self.assertEquals(view.func.view_class, StationGalleryListView)