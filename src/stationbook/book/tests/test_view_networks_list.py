from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import NetworksListView

class NetworksListTests(NetworkStationTest):
    def __init__(self, *args):
        pass
        # NetworkStationTest.__init__(
        #     self, *args, url='networks', arguments={})

    # def test_network_list_view_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)
    
    # def test_networks_list_url_resolves_view(self):
    #     view = resolve('/networks/')
    #     self.assertEquals(view.func.view_class, NetworksListView)