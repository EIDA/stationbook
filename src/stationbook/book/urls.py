from django.conf.urls import url
from django.urls import path, re_path
from book import views

urlpatterns = [
    path("", views.StationsListView.as_view(), name="home"),
]
