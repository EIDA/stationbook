NO_FDSNWS_DATA = 'n/a'
NSMAP = {'mw': 'http://www.fdsn.org/xml/station/1'}

# Single node instance wrapper
class NodeWrapper(object):
    def __init__(self, node):
        self.code = node.code
        self.description = node.description
        self.url_dataselect = node.url_dataselect
        self.url_station = node.url_station
        self.url_routing = node.url_routing
        self.url_wfcatalog = node.url_wfcatalog
        self.networks = []
    
    def build_url_station_station_level(self):
        return self.url_station + '?network={0}&level=station'
    
    def build_url_station_network_level(self):
        return self.url_station + '?network=*&level=network'
    
    def build_url_station_channel_level(self):
        return self.url_station + '?network={0}&station={1}&level=channel'


# Single network instance  wrapper and collection of stations
class NetworkWrapper(object):
    def __init__(self):
        self.code = NO_FDSNWS_DATA
        self.description = NO_FDSNWS_DATA
        self.start_date = NO_FDSNWS_DATA
        self.restricted_status = NO_FDSNWS_DATA
        self.stations = []


# Single station instance wrapper
class StationWrapper(object):
    def __init__(self):
        self.code = NO_FDSNWS_DATA
        self.latitude = NO_FDSNWS_DATA
        self.longitude = NO_FDSNWS_DATA
        self.elevation = NO_FDSNWS_DATA
        self.restricted_status = NO_FDSNWS_DATA
        self.start_date = NO_FDSNWS_DATA
        self.creation_date = NO_FDSNWS_DATA
        self.site_name = NO_FDSNWS_DATA


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