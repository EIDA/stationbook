from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import UserDetailsListView


class UserDetailsTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self, *args, url="user_details", arguments={"username": "admin"}
        )

    def test_user_details_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_user_details_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 200)

    def test_user_details_url_resolves_view(self):
        view = resolve("/user/admin/")
        self.assertEquals(view.func.view_class, UserDetailsListView)
