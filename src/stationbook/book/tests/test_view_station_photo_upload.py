from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..models import FdsnNetwork, FdsnStation, ExtEntityBase, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, \
ExtBoreholeData, ExtBoreholeLayerData

class StationPhotoUploadTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(self, *args, url='station_details')