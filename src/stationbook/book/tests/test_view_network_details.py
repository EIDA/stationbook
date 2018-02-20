from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import NetworkDetailsListView

class NetworkDetailsTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(
        #     self, *args, url='network_details',
        #     arguments={'network_code': 'NET'})
    
    # def test_network_details_view_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)

    # def test_network_details_url_resolves_view(self):
    #     view = resolve('/networks/NET/')
    #     self.assertEquals(view.func.view_class, NetworkDetailsListView)