from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import NetworkDetailsListView


class NetworkDetailsTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self,
            *args,
            url="network_details",
            arguments={"network_code": "NET", "network_start_year": "1990"}
        )

    def test_network_details_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_network_details_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_network_details_url_resolves_view(self):
        view = resolve("/networks/NET/1990/")
        self.assertEquals(view.func.view_class, NetworkDetailsListView)
