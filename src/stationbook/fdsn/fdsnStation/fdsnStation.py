from requests import ReadTimeout, ConnectTimeout, HTTPError,\
Timeout, ConnectionError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

class StationList(object):
    def __init__(self, network):
        self.url = 'http://orfeus-eu.org/fdsnws/station/1/query?network={0}'\
        .format(network.upper())
        self.NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}

    def get_station_collection(self):
        try:
            stationDict = {}
            response = urlopen(self.url)
            root = ET.fromstring(response.read())

            for station in root.findall('.//mw:Station', namespaces=self.NSMAP):
                site = station.find('.//mw:Name', namespaces=self.NSMAP).text

                latitude = station.find('.//mw:Latitude',
                                  namespaces=self.NSMAP).text

                longitude = station.find('.//mw:Longitude',
                                   namespaces=self.NSMAP).text

                stationDict[site] = {}
                stationDict[site]['lat'] = latitude
                stationDict[site]['lon'] = longitude

            return stationDict
        except (ConnectTimeout, HTTPError, ReadTimeout,
                Timeout, ConnectionError):
            pass

stat_list = StationList('nl')
stat_collection = stat_list.get_station_collection()