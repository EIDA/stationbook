from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import station_borehole_layer_remove


class StationBoreholeLayerRemoveTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self,
            *args,
            url="station_borehole_layer_remove",
            arguments={"network_pk": "1", "station_pk": "1", "layer_pk": "1"}
        )

    def test_station_borehole_layer_remove_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_station_borehole_layer_remove_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 302)

    def test_station_borehole_layer_remove_url_resolves_view(self):
        view = resolve("/networks/1/station/1/remove-borehole-layer/1/")
        self.assertEquals(view.func, station_borehole_layer_remove)
