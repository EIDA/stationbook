from pprint import pprint

from requests import \
ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from .fdsnws import NO_FDSNWS_DATA
from ..logger import StationBookLogger

class StationChannelsGraph(object):
    def __init__(self, network, station):
        self.url = 'http://orfeus-eu.org/fdsnws/station/1/query?network={0}&station={1}&level=channel'\
        .format(network.upper(), station.upper())
        self.NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}
    
    def get_station_channels(self):
        channels_graph = StationChannels()
        response = urlopen(self.url)

        http_code = response.getcode()

        # If something went wrong, log it and return empty dataset
        if http_code != 200:
            StationBookLogger(__name__).log_exception('{0} from {1} in {2}'.format(http_code, self.url, StationChannelsGraph.__name__))
            return StationChannels()

        root = ET.fromstring(response.read())

        try:
            for channel in root.findall(
                './/mw:Channel', namespaces=self.NSMAP):
                
                cha = StationChannel()
                cha.code = channel.get('code')
                cha.start_date = channel.get('startDate')
                cha.restricted_status = channel.get('restrictedStatus')
                cha.location_code = channel.get('locationCode')

                tmp = channel.find(
                    './/mw:Latitude', namespaces=self.NSMAP)
                if tmp != None:
                    cha.latitude = tmp.text

                tmp = channel.find(
                    './/mw:Longitude', namespaces=self.NSMAP)
                if tmp != None:
                    cha.longitude = tmp.text

                tmp = channel.find(
                    './/mw:Elevation', namespaces=self.NSMAP)
                if tmp != None:
                    cha.elevation = tmp.text

                tmp = channel.find(
                    './/mw:Depth', namespaces=self.NSMAP)
                if tmp != None:
                    cha.depth = tmp.text

                tmp = channel.find(
                    './/mw:Azimuth', namespaces=self.NSMAP)
                if tmp != None:
                    cha.azimuth = tmp.text

                tmp = channel.find(
                    './/mw:Dip', namespaces=self.NSMAP)
                if tmp != None:
                    cha.dip = tmp.text

                tmp = channel.find(
                    './/mw:SampleRate', namespaces=self.NSMAP)
                if tmp != None:
                    cha.sample_rate = tmp.text

                tmp = channel.find(
                    './/mw:StorageFormat', namespaces=self.NSMAP)
                if tmp != None:
                    cha.storage_format = tmp.text

                tmp = channel.find(
                    './/mw:ClockDrift', namespaces=self.NSMAP)
                if tmp != None:
                    cha.clock_drift = tmp.text
                
                tmp = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Type', namespaces=self.NSMAP)
                if tmp != None:
                    cha.sensor.type = tmp.text
                    
                tmp = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Manufacturer', namespaces=self.NSMAP)
                if tmp != None:
                    cha.sensor.manufacturer = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Manufacturer', namespaces=self.NSMAP).text
                
                tmp = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Description', namespaces=self.NSMAP)
                if tmp != None:
                    cha.sensor.description = tmp.text

                tmp = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Model', namespaces=self.NSMAP)
                if tmp != None:
                    cha.sensor.model = tmp.text

                tmp = channel.find(
                    './/mw:DataLogger', namespaces=self.NSMAP).find(
                        './/mw:Description', namespaces=self.NSMAP)
                if tmp != None:
                    cha.data_logger.description = tmp.text
                
                tmp = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:Value', namespaces=self.NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.value = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:Frequency', namespaces=self.NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.frequency = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:InputUnits', namespaces=self.NSMAP).find(
                                './/mw:Name', namespaces=self.NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.input_units.name = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:OutputUnits', namespaces=self.NSMAP).find(
                                './/mw:Name', namespaces=self.NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.output_units.name = tmp.text

                channels_graph.channels.append(cha)
            return channels_graph
        except:
            StationBookLogger(__name__).log_exception(
                StationChannelsGraph.__name__)
            return StationChannels()


class StationChannels(object):
    def __init__(self):
        self.channels = []
    
    def __str__(self):
        for c in self.channels:
            return c.__str__()


class StationChannel(object):
    def __init__(self):
        self.code = NO_FDSNWS_DATA
        self.start_date = NO_FDSNWS_DATA
        self.restricted_status = NO_FDSNWS_DATA
        self.location_code = NO_FDSNWS_DATA
        self.latitude = NO_FDSNWS_DATA
        self.longitude = NO_FDSNWS_DATA
        self.elevation = NO_FDSNWS_DATA
        self.depth = NO_FDSNWS_DATA
        self.azimuth = NO_FDSNWS_DATA
        self.dip = NO_FDSNWS_DATA
        self.sample_rate = NO_FDSNWS_DATA
        # self.sample_rate_ratio = StationChannelSampleRateRatio()
        self.storage_format = NO_FDSNWS_DATA
        self.clock_drift = NO_FDSNWS_DATA
        self.sensor = StationChannelSensor()
        self.data_logger = StationChannelDataLogger()
        self.response = StationChannelResponse()
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelSampleRateRatio(object):
    def __init__(self):
        self.number_samples = NO_FDSNWS_DATA
        self.number_seconds = NO_FDSNWS_DATA
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelSensor(object):
    def __init__(self):
        self.resource_id = NO_FDSNWS_DATA
        self.type = NO_FDSNWS_DATA
        self.manufacturer = NO_FDSNWS_DATA
        self.description = NO_FDSNWS_DATA
        self.model = NO_FDSNWS_DATA
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelDataLogger(object):
    def __init__(self):
        self.resource_id = NO_FDSNWS_DATA
        self.description = NO_FDSNWS_DATA
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelResponse(object):
    def __init__(self):
        self.instrument_sensitivity = StationChannelResponseInstrumentSensitivity()
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseInstrumentSensitivity(object):
    def __init__(self):
        self.value = NO_FDSNWS_DATA
        self.frequency = NO_FDSNWS_DATA
        self.input_units = StationChannelResponseInputUnits()
        self.output_units = StationChannelResponseOutputUnits()

    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseInputUnits(object):
    def __init__(self):
        self.name = NO_FDSNWS_DATA

    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseOutputUnits(object):
    def __init__(self):
        self.name = NO_FDSNWS_DATA

    def __str__(self):
        return pprint(vars(self))


if __name__ == '__main__':
    tst = StationChannelsGraph(network='CR', station='RABC')
    result = tst.get_station_channels()
    pprint(result)