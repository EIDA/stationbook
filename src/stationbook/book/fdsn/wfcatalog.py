from requests import \
ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from ..logger import StationBookLogger

class WfCatalogGraph(object):
    def __init__(self, network_code, station_code):
        self.net_code = network_code.upper()
        self.stat_code = station_code.upper()
        self.url = ''.format(nc=self.net_code, sc=self.stat_code)