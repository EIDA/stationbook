from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from pprint import pprint
from urllib.request import urlopen
import xml.etree.ElementTree as ET

class NetworkStationGraph(object):
    def __init__(self, network):
        self.url = 'http://orfeus-eu.org/fdsnws/station/1/query?network={0}'\
        .format(network.upper())
        self.NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}

    def get_network_station_graph(self):
        network_graph = Networks()
        response = urlopen(self.url)
        root = ET.fromstring(response.read())

        try:
            for network in root.findall('.//mw:Network', namespaces=self.NSMAP):
                network_code = network.get('code')
                network_start_date = network.get('startDate')
                network_restricted_status = network.get('restrictedStatus')
                network_description = network.find('.//mw:Description', namespaces=self.NSMAP).text

                network_graph_network = Network()
                network_graph_network.code = network_code
                network_graph_network.start_date = network_start_date
                network_graph_network.restricted_status = (network_restricted_status or 'unknown')
                network_graph_network.description = network_description

                network_graph.networks.append(network_graph_network)

                for station in network.findall('.//mw:Station', namespaces=self.NSMAP):
                    station_code = station.get('code')
                    station_start_date = station.get('startDate')
                    station_restricted_status = station.get('restrictedStatus')
                    station_site_name = station.find('.//mw:Name', namespaces=self.NSMAP).text
                    station_latitude = station.find('.//mw:Latitude', namespaces=self.NSMAP).text
                    station_longitude = station.find('.//mw:Longitude', namespaces=self.NSMAP).text
                    station_elevation = station.find('.//mw:Elevation', namespaces=self.NSMAP).text
                    station_creation_date = station.find('.//mw:CreationDate', namespaces=self.NSMAP).text

                    network_graph_network_station = Station()
                    network_graph_network_station.code = station_code
                    network_graph_network_station.latitude = station_latitude
                    network_graph_network_station.longitude = station_longitude
                    network_graph_network_station.elevation = station_elevation
                    network_graph_network_station.restricted_status = (station_restricted_status or 'unknown')
                    network_graph_network_station.start_date = station_start_date
                    network_graph_network_station.creation_date = station_creation_date
                    network_graph_network_station.site_name = station_site_name

                    network_graph_network.stations.append(network_graph_network_station)
        
            return network_graph
        except (ConnectTimeout, HTTPError, ReadTimeout,
                Timeout, ConnectionError):
            pass

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

if __name__ == "__main__":
    data = NetworkStationGraph('*')
    graph = data.get_network_station_graph()

    for network in graph.networks:
        pprint(vars(network))

        for station in network.stations:
            pprint(vars(station))
