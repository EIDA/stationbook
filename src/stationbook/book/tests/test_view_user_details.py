from django.urls import resolve, reverse

from .base_classes import NetworkStationTest

class UserDetailsTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(self, *args, url='user_details')