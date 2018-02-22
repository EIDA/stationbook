from django.urls import resolve, reverse

from .base_classes import NetworkStationTest
from ..views import RecentChangesListView

class RecentChangesTests(NetworkStationTest):
    def __init__(self, *args):
        NetworkStationTest.__init__(
            self, *args, url='recent_changes', arguments={})
    
    def test_recent_changes_view_status_code_authenticated(self):
        self.login_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_recent_changes_view_status_code_anon(self):
        self.logout_and_refresh()
        self.assertEquals(self.response.status_code, 200)
    
    def test_recent_changes_url_resolves_view(self):
        view = resolve('/recent_changes/')
        self.assertEquals(view.func.view_class, RecentChangesListView)