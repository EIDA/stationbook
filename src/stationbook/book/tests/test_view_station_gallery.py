from django.urls import resolve, reverse

from .base_classes import NetworkStationTest

class StationGalleryTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='station_gallery')