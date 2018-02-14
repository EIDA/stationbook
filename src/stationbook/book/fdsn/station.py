from requests import \
ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from django.db import transaction

from .background import BackgroundThread

from ..logger import StationBookLogger
from ..models import FdsnNetwork, FdsnStation, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, \
ExtHousingData, ExtAccessData, ExtBoreholeData, ExtBoreholeLayerData

class NetworkStationGraph(object):
    def __init__(self, network):
        self.url = 'http://orfeus-eu.org/fdsnws/station/1/query?network={0}'\
        .format(network.upper())
        self.NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}

    def get_network_station_graph(self):
        net_graph = Networks()
        response = urlopen(self.url)
        root = ET.fromstring(response.read())

        try:
            for network in root.findall(
                './/mw:Network',namespaces=self.NSMAP):

                net = Network()
                net.code = network.get('code')
                net.start_date = network.get('startDate')
                net.restricted_status = (
                    network.get('restrictedStatus') or 'unknown')
                net.description = network.find(
                    './/mw:Description', namespaces=self.NSMAP).text

                net_graph.networks.append(net)

                for station in network.findall(
                    './/mw:Station', namespaces=self.NSMAP):

                    stat = Station()
                    stat.code = station.get('code')
                    stat.latitude = station.find(
                        './/mw:Latitude', namespaces=self.NSMAP).text
                    stat.longitude = station.find(
                        './/mw:Longitude', namespaces=self.NSMAP).text
                    stat.elevation = station.find(
                        './/mw:Elevation', namespaces=self.NSMAP).text
                    stat.restricted_status = (
                        station.get('restrictedStatus') or 'unknown')
                    stat.start_date = station.get('startDate')
                    stat.creation_date = station.find(
                        './/mw:CreationDate', namespaces=self.NSMAP).text
                    stat.site_name = station.find(
                        './/mw:Name', namespaces=self.NSMAP).text

                    net.stations.append(stat)
        
            return net_graph
        except:
            StationBookLogger(__name__).log_exception(
                NetworkStationGraph.__name__)

# Collection of networks
class Networks(object):
    def __init__(self):
        self.networks = []

# Single network instance and collection of stations
class Network(object):
    def __init__(self):
        self.code = ''
        self.name = ''
        self.description = ''
        self.start_date = ''
        self.restricted_status = ''
        self.stations = []

# Single station instance
class Station(object):
    def __init__(self):
        self.code = ''
        self.latitude = 0
        self.longitude = 0
        self.elevation = 0
        self.restricted_status = ''
        self.start_date = ''
        self.creation_date = ''
        self.site_name = ''

def _refresh_station():
    try:
        data = NetworkStationGraph('*')
        graph = data.get_network_station_graph()

        for network in graph.networks:
            # If network is known in the database, just update it with the
            # latest FDSN data, otherwise add it to the database
            if FdsnNetwork.objects.filter(code=network.code).exists():
                net = FdsnNetwork.objects.get(code=network.code)
                net.name = network.name
                net.description = network.description
                net.start_date = network.start_date
                net.restricted_status = network.restricted_status
                net.save()
            else:
                net = FdsnNetwork()
                net.code = network.code
                net.name = network.name
                net.description = network.description
                net.start_date = network.start_date
                net.restricted_status = network.restricted_status
                net.save()

            for station in network.stations:
                # If station is known in the database, just update it with the
                # latest FDSN data, otherwise add it to the database
                if FdsnStation.objects.filter(code=station.code).exists():
                    stat = FdsnStation.objects.get(code=station.code)
                    stat.latitude = station.latitude
                    stat.longitude = station.longitude
                    stat.elevation = station.elevation
                    stat.restricted_status = station.restricted_status
                    stat.start_date = station.start_date
                    stat.creation_date = station.creation_date
                    stat.site_name = station.site_name
                    stat.save()
                else:
                    # Create station entity
                    stat = FdsnStation()
                    # Assign station to network
                    stat.fdsnStation_fdsnNetwork = net
                    # Fill data obtained from the Web Service
                    stat.code = station.code
                    stat.latitude = station.latitude
                    stat.longitude = station.longitude
                    stat.elevation = station.elevation
                    stat.restricted_status = station.restricted_status
                    stat.start_date = station.start_date
                    stat.creation_date = station.creation_date
                    stat.site_name = station.site_name
                    # Create ext entities
                    ext_data = ExtBasicData()
                    ext_owner = ExtOwnerData()
                    ext_morphology = ExtMorphologyData()
                    ext_housing = ExtHousingData()
                    ext_borehole = ExtBoreholeData()
                    
                    # Assign ext entities to station and save it
                    try:
                        with transaction.atomic():
                            ext_data.save()
                            ext_owner.save()
                            ext_morphology.save()
                            ext_housing.save()
                            ext_borehole.save()
                            
                            stat.ext_basic_data = ext_data
                            stat.ext_owner_data = ext_owner
                            stat.ext_morphology_data = ext_morphology
                            stat.ext_housing_data = ext_housing
                            stat.ext_borehole_data = ext_borehole
                            stat.save()
                    except:
                        StationBookLogger(__name__).log_exception(
                            _refresh_station.__name__)
    except:
        StationBookLogger(__name__).log_exception(
            _refresh_station.__name__)

def refresh_station_in_thread():
    worker = BackgroundThread(_refresh_station)
    worker.run()