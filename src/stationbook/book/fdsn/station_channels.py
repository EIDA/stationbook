from pprint import pprint

from requests import \
ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from ..logger import StationBookLogger

class StationChannelsGraph(object):
    def __init__(self, network, station):
        self.url = 'http://orfeus-eu.org/fdsnws/station/1/query?network={0}&station={1}&level=channel'\
        .format(network.upper(), station.upper())
        self.NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}
    
    def get_station_channels(self):
        channels_graph = StationChannels()
        response = urlopen(self.url)
        root = ET.fromstring(response.read())

        try:
            for channel in root.findall(
                './/mw:Channel', namespaces=self.NSMAP):
                
                cha = StationChannel()
                cha.code = channel.get('code')
                cha.start_date = channel.get('startDate')
                cha.restricted_status = channel.get('restrictedStatus')
                cha.location_code = channel.get('locationCode')
                cha.latitude = channel.find(
                    './/mw:Latitude', namespaces=self.NSMAP).text
                cha.longitude = channel.find(
                    './/mw:Longitude', namespaces=self.NSMAP).text
                cha.elevation = channel.find(
                    './/mw:Elevation', namespaces=self.NSMAP).text
                cha.depth = channel.find(
                    './/mw:Depth', namespaces=self.NSMAP).text
                cha.azimuth = channel.find(
                    './/mw:Azimuth', namespaces=self.NSMAP).text
                cha.dip = channel.find(
                    './/mw:Dip', namespaces=self.NSMAP).text
                cha.sample_rate = channel.find(
                    './/mw:SampleRate', namespaces=self.NSMAP).text
                cha.storage_format = channel.find(
                    './/mw:StorageFormat', namespaces=self.NSMAP).text
                cha.clock_drift = channel.find(
                    './/mw:ClockDrift', namespaces=self.NSMAP).text
                
                cha.sensor.type = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Type', namespaces=self.NSMAP).text

                cha.sensor.description = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Description', namespaces=self.NSMAP).text

                cha.sensor.model = channel.find(
                    './/mw:Sensor', namespaces=self.NSMAP).find(
                        './/mw:Model', namespaces=self.NSMAP).text

                cha.data_logger.description = channel.find(
                    './/mw:DataLogger', namespaces=self.NSMAP).find(
                        './/mw:Description', namespaces=self.NSMAP).text
                
                cha.response.instrument_sensitivity.value = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:Value', namespaces=self.NSMAP).text

                cha.response.instrument_sensitivity.frequency = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:Frequency', namespaces=self.NSMAP).text

                cha.response.instrument_sensitivity.input_units.name = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:InputUnits', namespaces=self.NSMAP).find(
                                './/mw:Name', namespaces=self.NSMAP).text

                cha.response.instrument_sensitivity.output_units.name = channel.find(
                    './/mw:Response', namespaces=self.NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=self.NSMAP).find(
                            './/mw:OutputUnits', namespaces=self.NSMAP).find(
                                './/mw:Name', namespaces=self.NSMAP).text

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
        self.code = ''
        self.start_date = ''
        self.restricted_status = ''
        self.location_code = ''
        self.latitude = ''
        self.longitude = ''
        self.elevation = ''
        self.depth = ''
        self.azimuth = ''
        self.dip = ''
        self.sample_rate = ''
        # self.sample_rate_ratio = StationChannelSampleRateRatio()
        self.storage_format = ''
        self.clock_drift = ''
        self.sensor = StationChannelSensor()
        self.data_logger = StationChannelDataLogger()
        self.response = StationChannelResponse()
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelSampleRateRatio(object):
    def __init__(self):
        self.number_samples = 0
        self.number_seconds = 0
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelSensor(object):
    def __init__(self):
        self.resource_id = ''
        self.type = ''
        self.description = ''
        self.model = ''
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelDataLogger(object):
    def __init__(self):
        self.resource_id = ''
        self.description = ''
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelResponse(object):
    def __init__(self):
        self.instrument_sensitivity = StationChannelResponseInstrumentSensitivity()
    
    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseInstrumentSensitivity(object):
    def __init__(self):
        self.value = ''
        self.frequency = ''
        self.input_units = StationChannelResponseInputUnits()
        self.output_units = StationChannelResponseOutputUnits()

    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseInputUnits(object):
    def __init__(self):
        self.name = ''

    def __str__(self):
        return pprint(vars(self))


class StationChannelResponseOutputUnits(object):
    def __init__(self):
        self.name = ''

    def __str__(self):
        return pprint(vars(self))


if __name__ == '__main__':
    tst = StationChannelsGraph(network='CR', station='RABC')
    result = tst.get_station_channels()
    pprint(result)