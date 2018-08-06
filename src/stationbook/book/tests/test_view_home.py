from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import HomeListView

class HomeTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self,
            *args,
            url='home',
            arguments={}
        )

    def test_home_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, HomeListView)

    def test_home_view_contains_link_to_station_page(self):
        home_url = reverse('home')