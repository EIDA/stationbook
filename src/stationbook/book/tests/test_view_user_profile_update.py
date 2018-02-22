from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import update_profile

class UserProfileUpdateTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self, *args, url='my_account', arguments={})

    def test_user_profile_update_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_profile_update_url_resolves_view(self):
        view = resolve('/settings/account/')
        self.assertEquals(view.func, update_profile)