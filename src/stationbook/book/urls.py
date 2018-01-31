from django.conf.urls import url
from django.urls import path
from book import views

urlpatterns = [
    path('', views.StationListView.as_view(), name='home'),
]