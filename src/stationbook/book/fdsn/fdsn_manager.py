# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen
import gzip
from .background import BackgroundThread

from django.db import transaction

from .base_classes import \
NO_FDSNWS_DATA, NSMAP, NodeWrapper, NetworkWrapper, StationWrapper, \
StationChannels, StationChannel, StationChannelSampleRateRatio, \
StationChannelSensor, StationChannelDataLogger, StationChannelResponse, \
StationChannelResponseInstrumentSensitivity, \
StationChannelResponseInputUnits, StationChannelResponseOutputUnits

from ..logger import StationBookLogger
from ..models import \
FdsnNode, FdsnNetwork, FdsnStation, ExtBasicData, ExtOwnerData, \
ExtMorphologyData, ExtHousingData, ExtAccessData, ExtBoreholeData, \
ExtBoreholeLayerData

class FdsnNetworkManager(object):
    def __init__(self):
        pass

    def fdsn_request(self, url):
        try:
            req = Request(url)
            req.add_header('Accept-Encoding', 'gzip')
            response = urlopen(req)
            
            if response.info().get('Content-Encoding') == 'gzip':
                return gzip.decompress(response.read())
            else:
                return response.read()
        except Exception:
            raise

    def _get_fdsn_nodes(self):
        try:
            for n in FdsnNode.objects.all():
                yield NodeWrapper(n)
        except:
            raise
    
    def _discover_node_networks(self, node_wrapper):
        try:
            response = self.fdsn_request(
                node_wrapper.build_url_station_network_level())
            root = ET.fromstring(response)

            for network in root.findall('.//mw:Network', namespaces=NSMAP):
                net_wrapper = NetworkWrapper()
                net_wrapper.code = network.get('code')
                net_wrapper.start_date = network.get('startDate')
                net_wrapper.restricted_status = (
                    network.get('restrictedStatus') or 'unknown')
                net_wrapper.description = network.find(
                    './/mw:Description', namespaces=NSMAP).text

                yield net_wrapper
        except ParseError:
            StationBookLogger(__name__).log_exception(
                FdsnNetworkManager.__name__)
        except:
            raise

    def _save_node_network(self, node_wrapper, network_wrapper):
        try:
            if FdsnNetwork.objects.filter(
                fdsn_node__code=node_wrapper.code, 
                code=network_wrapper.code).exists():
            
                net = FdsnNetwork.objects.get(code=network_wrapper.code)
                net.description = network_wrapper.description
                net.start_date = network_wrapper.start_date
                net.restricted_status = network_wrapper.restricted_status
                net.save()
            else:
                net = FdsnNetwork()
                net.code = network_wrapper.code
                net.description = network_wrapper.description
                net.start_date = network_wrapper.start_date
                net.restricted_status = network_wrapper.restricted_status
                net.fdsn_node = FdsnNode.objects.get(
                    code=node_wrapper.code)
                net.save()
        except:
            StationBookLogger(__name__).log_exception(
                'Class: {0}, Node: {1}, Network: {2}'.format(
                    FdsnNetworkManager.__name__, 
                    node_wrapper.code, 
                    network_wrapper.code))
    
    def _discover_network_stations(self, node_wrapper, network_wrapper):
        try:
            response = self.fdsn_request(
                node_wrapper.build_url_station_station_level().format(
                    network_wrapper.code.upper()))
            root = ET.fromstring(response)

            for station in root.find(
                './/mw:Network', namespaces=NSMAP).findall(
                    './/mw:Station', namespaces=NSMAP):
                stat_wrapper = StationWrapper()

                tmp = station.get('code')
                if tmp != None:
                    stat_wrapper.code = tmp

                tmp = station.find(
                    './/mw:Latitude', namespaces=NSMAP).text
                if tmp != None:
                    stat_wrapper.latitude = tmp
                
                if tmp != None:
                    stat_wrapper.longitude = station.find(
                        './/mw:Longitude', namespaces=NSMAP).text
                
                tmp = station.find(
                    './/mw:Elevation', namespaces=NSMAP).text
                if tmp != None:
                    stat_wrapper.elevation = tmp
                
                tmp = station.get('restrictedStatus') or 'unknown'
                if tmp != None:
                    stat_wrapper.restricted_status = tmp
                
                tmp = station.get('startDate')
                if tmp != None:
                    stat_wrapper.start_date = tmp
                
                tmp = station.find(
                    './/mw:CreationDate', namespaces=NSMAP).text
                if tmp != None:
                    stat_wrapper.creation_date = tmp
                
                tmp = station.find(
                    './/mw:Site', namespaces=NSMAP).find(
                        './/mw:Name', namespaces=NSMAP).text
                if tmp != None:
                    stat_wrapper.site_name = tmp

                yield stat_wrapper
        except ParseError:
            StationBookLogger(__name__).log_exception(
                FdsnNetworkManager.__name__)
        except:
            raise

    def _save_network_station(self, node_wrapper, network_wrapper, station_wrapper):
        try:
            # If station is known in the database, just update it with the
            # latest FDSN data, otherwise add it to the database
            if FdsnStation.objects.filter(code=station_wrapper.code).exists():
                stat = FdsnStation.objects.get(code=station_wrapper.code)
                stat.latitude = station_wrapper.latitude
                stat.longitude = station_wrapper.longitude
                stat.elevation = station_wrapper.elevation
                stat.restricted_status = station_wrapper.restricted_status
                stat.start_date = station_wrapper.start_date
                stat.creation_date = station_wrapper.creation_date
                stat.site_name = station_wrapper.site_name
                stat.save()
            else:
                # Create station entity
                stat = FdsnStation()
                # Assign station to network
                stat.fdsn_network = FdsnNetwork.objects.get(
                    code=network_wrapper.code)
                # Fill data obtained from the Web Service
                stat.code = station_wrapper.code
                stat.latitude = station_wrapper.latitude
                stat.longitude = station_wrapper.longitude
                stat.elevation = station_wrapper.elevation
                stat.restricted_status = station_wrapper.restricted_status
                stat.start_date = station_wrapper.start_date
                stat.creation_date = station_wrapper.creation_date
                stat.site_name = station_wrapper.site_name
                # Create ext entities
                ext_basic = ExtBasicData()
                ext_owner = ExtOwnerData()
                ext_morphology = ExtMorphologyData()
                ext_housing = ExtHousingData()
                ext_borehole = ExtBoreholeData()
                
                # Assign ext entities to station and save it
                try:
                    with transaction.atomic():
                        ext_basic.save()
                        ext_owner.save()
                        ext_morphology.save()
                        ext_housing.save()
                        ext_borehole.save()
                        
                        stat.ext_basic_data = ext_basic
                        stat.ext_owner_data = ext_owner
                        stat.ext_morphology_data = ext_morphology
                        stat.ext_housing_data = ext_housing
                        stat.ext_borehole_data = ext_borehole
                        stat.save()
                except:
                    StationBookLogger(__name__).log_exception(
                        FdsnNetworkManager.__name__)
        except:
            raise
    
    def discover_station_channels(self, network_code, station_code):
        try:
            network = FdsnNetwork.objects.get(code=network_code)
            node_wrapper = NodeWrapper(network.fdsn_node)
            channels_graph = StationChannels()

            response = self.fdsn_request(
                node_wrapper.build_url_station_channel_level().format(
                    network_code.upper(), station_code.upper()))
            root = ET.fromstring(response)

            for channel in root.findall('.//mw:Channel', namespaces=NSMAP):
                cha = StationChannel()

                tmp = channel.get('code')
                if tmp != None:
                    cha.code = tmp

                tmp = channel.get('startDate')
                if tmp != None:
                    cha.start_date = tmp

                tmp = channel.get('restrictedStatus')
                if tmp != None:
                    cha.restricted_status = tmp

                tmp = channel.get('locationCode')
                if tmp != None:
                    cha.location_code = tmp

                tmp = channel.find(
                    './/mw:Latitude', namespaces=NSMAP)
                if tmp != None:
                    cha.latitude = tmp.text

                tmp = channel.find(
                    './/mw:Longitude', namespaces=NSMAP)
                if tmp != None:
                    cha.longitude = tmp.text

                tmp = channel.find(
                    './/mw:Elevation', namespaces=NSMAP)
                if tmp != None:
                    cha.elevation = tmp.text

                tmp = channel.find(
                    './/mw:Depth', namespaces=NSMAP)
                if tmp != None:
                    cha.depth = tmp.text

                tmp = channel.find(
                    './/mw:Azimuth', namespaces=NSMAP)
                if tmp != None:
                    cha.azimuth = tmp.text

                tmp = channel.find(
                    './/mw:Dip', namespaces=NSMAP)
                if tmp != None:
                    cha.dip = tmp.text

                tmp = channel.find(
                    './/mw:SampleRate', namespaces=NSMAP)
                if tmp != None:
                    cha.sample_rate = tmp.text

                tmp = channel.find(
                    './/mw:StorageFormat', namespaces=NSMAP)
                if tmp != None:
                    cha.storage_format = tmp.text

                tmp = channel.find(
                    './/mw:ClockDrift', namespaces=NSMAP)
                if tmp != None:
                    cha.clock_drift = tmp.text
                
                tmp = channel.find(
                    './/mw:Sensor', namespaces=NSMAP).find(
                        './/mw:Type', namespaces=NSMAP)
                if tmp != None:
                    cha.sensor.type = tmp.text
                    
                tmp = channel.find(
                    './/mw:Sensor', namespaces=NSMAP).find(
                        './/mw:Manufacturer', namespaces=NSMAP)
                if tmp != None:
                    cha.sensor.manufacturer = channel.find(
                    './/mw:Sensor', namespaces=NSMAP).find(
                        './/mw:Manufacturer', namespaces=NSMAP).text
                
                tmp = channel.find(
                    './/mw:Sensor', namespaces=NSMAP).find(
                        './/mw:Description', namespaces=NSMAP)
                if tmp != None:
                    cha.sensor.description = tmp.text

                tmp = channel.find(
                    './/mw:Sensor', namespaces=NSMAP).find(
                        './/mw:Model', namespaces=NSMAP)
                if tmp != None:
                    cha.sensor.model = tmp.text

                tmp = channel.find(
                    './/mw:DataLogger', namespaces=NSMAP).find(
                        './/mw:Description', namespaces=NSMAP)
                if tmp != None:
                    cha.data_logger.description = tmp.text
                
                tmp = channel.find(
                    './/mw:Response', namespaces=NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=NSMAP).find(
                            './/mw:Value', namespaces=NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.value = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=NSMAP).find(
                            './/mw:Frequency', namespaces=NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.frequency = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=NSMAP).find(
                            './/mw:InputUnits', namespaces=NSMAP).find(
                                './/mw:Name', namespaces=NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.input_units.name = tmp.text

                tmp = channel.find(
                    './/mw:Response', namespaces=NSMAP).find(
                        './/mw:InstrumentSensitivity', namespaces=NSMAP).find(
                            './/mw:OutputUnits', namespaces=NSMAP).find(
                                './/mw:Name', namespaces=NSMAP)
                if tmp != None:
                    cha.response.instrument_sensitivity.output_units.name = tmp.text

                channels_graph.channels.append(cha)

            return channels_graph
        except ParseError:
            StationBookLogger(__name__).log_exception(
                FdsnNetworkManager.__name__)
        except:
            StationBookLogger(__name__).log_exception(
                FdsnNetworkManager.__name__)
            return StationChannels()

    def _process_fdsn_networks(self):
        try:
            for node_wrapper in self._get_fdsn_nodes():
                for network_wrapper in self._discover_node_networks(node_wrapper):
                    self._save_node_network(node_wrapper, network_wrapper)
        except:
            raise
    
    def _process_fdsn_stations(self):
        try:
            for node_wrapper in self._get_fdsn_nodes():
                for network_wrapper in self._discover_node_networks(node_wrapper):
                    for station_wrapper in self._discover_network_stations(node_wrapper, network_wrapper):
                        self._save_network_station(node_wrapper, network_wrapper, station_wrapper)
        except:
            raise
    
    def _process_fdsn(self):
        self._process_fdsn_networks()
        self._process_fdsn_stations()
    
    def process_fdsn_in_thread(self):
        worker = BackgroundThread(self._process_fdsn())
        worker.run()