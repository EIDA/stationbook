# -*- coding: utf-8 -*-
import certifi
import ssl
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen
import gzip
from .background import BackgroundThread

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone, dateparse

from .base_classes import (
    NO_FDSNWS_DATA,
    NSMAP,
    RouteWrapper,
    RouteDatacenterWrapper,
    RouteParamWrapper,
    NodeWrapper,
    NetworkWrapper,
    StationWrapper,
    StationChannels,
    StationChannel,
    StationChannelSampleRateRatio,
    StationChannelSensor,
    StationChannelDataLogger,
    StationChannelResponse,
    StationChannelResponseInstrumentSensitivity,
    StationChannelResponseInputUnits,
    StationChannelResponseOutputUnits,
)

from ..logger import StationBookLoggerMixin
from ..models import (
    FdsnNode,
    FdsnNetwork,
    FdsnStation,
    ExtBasicData,
    ExtOwnerData,
    ExtMorphologyData,
    ExtHousingData,
    ExtAccessData,
    ExtBoreholeData,
    ExtBoreholeLayerData,
    Photo,
)


def create_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(certifi.where())
    return context

ssl._create_default_https_context = create_context

class FdsnHttpBase(StationBookLoggerMixin):
    def __init__(self):
        super(FdsnHttpBase, self).__init__()

    def fdsn_request(self, url):
        try:
            req = Request(url)
            req.add_header("Accept-Encoding", "gzip")
            response = urlopen(req)

            if response.info().get("Content-Encoding") == "gzip":
                return gzip.decompress(response.read())
            else:
                return response.read()
        except Exception:
            self.log_exception(url)
            return None

    def _get_fdsn_nodes(self):
        try:
            for n in FdsnNode.objects.all():
                yield NodeWrapper(n)
        except Exception:
            self.log_exception()
            raise

    def get_node_entity_based_on_url(self, url):
        try:
            # >>> x = 'http://geofon.gfz-potsdam.de/fdsnws/dataselect/1/query'
            # >>> x.split('/')[2]
            # 'geofon.gfz-potsdam.de'
            return FdsnNode.objects.filter(
                url_station__contains=url.split("/")[2]
            ).first()
        except FdsnNode.DoesNotExist:
            self.log_exception("Could not identify node based on url: {0}".format(url))
            return None
        except FdsnNode.MultipleObjectsReturned:
            self.log_exception("Multiple nodes returned based on url: {0}".format(url))
            return None
        except Exception:
            self.log_exception()
            raise

    def get_network_if_known(self, node_wrapper, network_wrapper):
        try:
            return FdsnNetwork.objects.get(
                fdsn_node__code=node_wrapper.code,
                code=network_wrapper.code,
                start_date__year=network_wrapper.parse_start_date_year(),
            )

        except FdsnNetwork.DoesNotExist:
            return None
        except Exception:
            self.log_exception()
            raise

    def get_station_if_known(self, network_wrapper, station_wrapper):
        try:
            return FdsnStation.objects.get(
                fdsn_network__code=network_wrapper.code,
                fdsn_network__start_date__year=network_wrapper.parse_start_date_year(),
                code=station_wrapper.code,
                start_date__year=station_wrapper.parse_start_date_year(),
            )

        except FdsnStation.DoesNotExist:
            return None
        except Exception:
            self.log_exception()
            raise

    def get_ext_if_known(self, T, network_wrapper, station_wrapper):
        try:
            return T.objects.get(
                ext_network_code=network_wrapper.code,
                ext_network_start_year=network_wrapper.parse_start_date_year(),
                ext_station_code=station_wrapper.code,
                ext_station_start_year=station_wrapper.parse_start_date_year(),
            )
        except T.DoesNotExist:
            return None
        except Exception:
            self.log_exception()
            raise

    def validate_string(self, string):
        if not string or len(string) <= 0:
            return NO_FDSNWS_DATA
        else:
            return string

    def make_dt_str_aware(self, dt_str):
        """Take a string containg a (possibly) naive datetime, and return a
           timezone-aware version of it, using the default timezone (should
           be UTC)."""
        # No date is still no data
        if dt_str == NO_FDSNWS_DATA:
            return NO_FDSNWS_DATA

        # Parse input date
        input_date = dateparse.parse_datetime(dt_str)

        # If naive, convert to aware
        if timezone.is_naive(input_date):
            aware_date = input_date.replace(tzinfo=timezone.get_default_timezone())

            # Convert it back to string for compatibilty
            return aware_date.isoformat()

        # Input was already timezone-aware, return it back
        return dt_str


class FdsnNetworkManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnNetworkManager, self).__init__()

    def _discover_node_networks(self, node_wrapper):
        try:
            response = self.fdsn_request(node_wrapper.build_url_station_network_level())

            if not response:
                return

            root = ET.fromstring(response)

            for network in root.findall(".//mw:Network", namespaces=NSMAP):
                net_wrapper = NetworkWrapper()

                tmp = network.get("code")
                if tmp is not None:
                    net_wrapper.code = self.validate_string(tmp)
                else:
                    self.log_warning(
                        "Network with no code received \
                        when discovering node networks!"
                    )
                    continue

                tmp = network.get("startDate")
                if tmp is not None:
                    tmp_date_str = self.validate_string(tmp)
                    net_wrapper.start_date = self.make_dt_str_aware(tmp_date_str)
                else:
                    self.log_warning(
                        "Network with no startDate received \
                        when discovering node networks!"
                    )
                    continue

                tmp = network.get("restrictedStatus")
                if tmp is not None:
                    net_wrapper.restricted_status = self.validate_string(tmp)

                tmp = network.find(".//mw:Description", namespaces=NSMAP)
                if tmp is not None:
                    net_wrapper.description = self.validate_string(tmp.text)

                yield net_wrapper
        except ParseError:
            self.log_exception()
        except Exception:
            self.log_exception()
            raise

    def _save_node_network(self, node_wrapper, network_wrapper):
        try:
            net = self.get_network_if_known(node_wrapper, network_wrapper)

            if net:
                net.description = network_wrapper.description
                # net.start_date = network_wrapper.start_date
                net.restricted_status = network_wrapper.restricted_status
                net.save()
            else:
                self.log_information(
                    "Adding: node {0} Network {1} Year {2}".format(
                        node_wrapper.code,
                        network_wrapper.code,
                        network_wrapper.parse_start_date_year(),
                    )
                )

                net = FdsnNetwork()
                net.code = network_wrapper.code
                net.description = network_wrapper.description
                net.start_date = network_wrapper.start_date
                net.restricted_status = network_wrapper.restricted_status
                net.fdsn_node = FdsnNode.objects.get(code=node_wrapper.code)
                net.save()
        except Exception:
            self.log_exception(
                "Node: {0} Network: {1}".format(
                    vars(node_wrapper), vars(network_wrapper)
                )
            )
            raise

    def _sync_fdsn_networks(self):
        try:
            for node_wrapper in self._get_fdsn_nodes():
                for network_wrapper in self._discover_node_networks(node_wrapper):
                    self._save_node_network(node_wrapper, network_wrapper)
        except Exception:
            self.log_exception()
            raise


class FdsnStationChannelsManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnStationChannelsManager, self).__init__()

    def discover_station_channels(self, network_pk, station_pk):
        try:
            network = FdsnNetwork.objects.get(pk=network_pk)
            station = FdsnStation.objects.get(pk=station_pk)
            node_wrapper = NodeWrapper(network.fdsn_node)
            channels_graph = StationChannels()

            response = self.fdsn_request(
                node_wrapper.build_url_station_channel_level().format(
                    network.code.upper(), station.code.upper()
                )
            )
            root = ET.fromstring(response)

            for channel in root.findall(".//mw:Channel", namespaces=NSMAP):
                cha = StationChannel()

                tmp = channel.get("code")
                if tmp is not None:
                    cha.code = self.validate_string(tmp)

                tmp = channel.get("startDate")
                if tmp is not None:
                    tmp_date_str = self.validate_string(tmp)
                    cha.start_date = self.make_dt_str_aware(tmp_date_str)

                tmp = channel.get("restrictedStatus")
                if tmp is not None:
                    cha.restricted_status = self.validate_string(tmp)

                tmp = channel.get("locationCode")
                if tmp is not None:
                    cha.location_code = self.validate_string(tmp)

                tmp = channel.find(".//mw:Latitude", namespaces=NSMAP)
                if tmp is not None:
                    cha.latitude = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Longitude", namespaces=NSMAP)
                if tmp is not None:
                    cha.longitude = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Elevation", namespaces=NSMAP)
                if tmp is not None:
                    cha.elevation = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Depth", namespaces=NSMAP)
                if tmp is not None:
                    cha.depth = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Azimuth", namespaces=NSMAP)
                if tmp is not None:
                    cha.azimuth = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Dip", namespaces=NSMAP)
                if tmp is not None:
                    cha.dip = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:SampleRate", namespaces=NSMAP)
                if tmp is not None:
                    cha.sample_rate = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:StorageFormat", namespaces=NSMAP)
                if tmp is not None:
                    cha.storage_format = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:ClockDrift", namespaces=NSMAP)
                if tmp is not None:
                    cha.clock_drift = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Sensor//mw:Type", namespaces=NSMAP)
                if tmp is not None:
                    cha.sensor.type = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Sensor//mw:Manufacturer", namespaces=NSMAP)
                if tmp is not None:
                    cha.sensor.manufacturer = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Sensor//mw:Description", namespaces=NSMAP)
                if tmp is not None:
                    cha.sensor.description = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:Sensor//mw:Model", namespaces=NSMAP)
                if tmp is not None:
                    cha.sensor.model = self.validate_string(tmp.text)

                tmp = channel.find(".//mw:DataLogger//mw:Description", namespaces=NSMAP)
                if tmp is not None:
                    cha.data_logger.description = self.validate_string(tmp.text)

                tmp = channel.find(
                    ".//mw:Response//mw:InstrumentSensitivity/mw:Value",
                    namespaces=NSMAP,
                )
                if tmp is not None:
                    cha.response.instrument_sensitivity.value = self.validate_string(
                        tmp.text
                    )

                tmp = channel.find(
                    ".//mw:Response//mw:InstrumentSensitivity//mw:Frequency",
                    namespaces=NSMAP,
                )
                if tmp is not None:
                    cha.response.instrument_sensitivity.frequency = self.validate_string(
                        tmp.text
                    )

                tmp = channel.find(
                    ".//mw:Response//mw:InstrumentSensitivity//mw:InputUnits//mw:Name",
                    namespaces=NSMAP,
                )
                if tmp is not None:
                    cha.response.instrument_sensitivity.input_units.name = self.validate_string(
                        tmp.text
                    )

                tmp = channel.find(
                    ".//mw:Response//mw:InstrumentSensitivity//mw:OutputUnits//mw:Name",
                    namespaces=NSMAP,
                )
                if tmp is not None:
                    cha.response.instrument_sensitivity.output_units.name = self.validate_string(
                        tmp.text
                    )

                channels_graph.channels.append(cha)

            return channels_graph
        except ParseError:
            self.log_exception()
            return StationChannels()
        except Exception:
            self.log_exception()
            return StationChannels()


class FdsnRoutingManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnRoutingManager, self).__init__()
        self.netman = FdsnNetworkManager()
        self.routing_node_wrapper = NodeWrapper(FdsnNode.objects.get(code="ODC"))

    def build_fdsn_station_url(self, url, param_wrapper):
        return url + "?network={0}&station={1}".format(
            param_wrapper.net.upper(), param_wrapper.sta.upper()
        )

    def _get_fdsn_networks(self):
        try:
            for n in FdsnNetwork.objects.order_by("code").values("code").distinct():
                yield n["code"]
        except Exception:
            self.log_exception()
            raise

    def _discover_network_routes(self, network_code):
        try:
            self.log_information(
                "Discovering network routes: {0}".format(
                    self.routing_node_wrapper.build_url_routing_network_level(
                        network_code
                    )
                )
            )

            response = self.fdsn_request(
                self.routing_node_wrapper.build_url_routing_network_level(network_code)
            )

            if not response:
                return

            root = ET.fromstring(response)

            route_wrapper = RouteWrapper()
            for dc in root.findall(".//datacenter"):
                datacenter_wrapper = RouteDatacenterWrapper()
                datacenter_wrapper.url = dc.find("url").text

                for param in dc.findall(".//params"):
                    param_wrapper = RouteParamWrapper()

                    tmp = param.find("loc").text
                    if tmp is not None:
                        param_wrapper.loc = tmp

                    tmp = param.find("end").text
                    if tmp is not None:
                        param_wrapper.end = tmp

                    tmp = param.find("sta").text
                    if tmp is not None:
                        param_wrapper.sta = tmp

                    tmp = param.find("cha").text
                    if tmp is not None:
                        param_wrapper.cha = tmp

                    tmp = param.find("priority").text
                    if tmp is not None:
                        param_wrapper.priority = tmp

                    tmp = param.find("start").text
                    if tmp is not None:
                        param_wrapper.start = tmp

                    tmp = param.find("net").text
                    if tmp is not None:
                        param_wrapper.net = tmp

                    yield datacenter_wrapper.url, param_wrapper

            return route_wrapper
        except ParseError:
            self.log_exception()
        except Exception:
            self.log_exception()
            raise

    def _discover_network_stations(self, url, param_wrapper):
        try:
            node_entity = self.get_node_entity_based_on_url(url)

            if not node_entity:
                self.log_warning("Node not configured for: {0}".format(url))
                return

            node_wrapper = NodeWrapper(node_entity)

            response = self.fdsn_request(
                node_wrapper.build_url_station_network_station_level(
                    param_wrapper.net, param_wrapper.sta
                )
            )

            if not response:
                return

            root = ET.fromstring(response)

            for network in root.findall(".//mw:Network", namespaces=NSMAP):
                network_wrapper = NetworkWrapper()

                tmp = network.get("startDate")
                if tmp is not None:
                    tmp_date_str = self.validate_string(tmp)
                    network_wrapper.start_date = self.make_dt_str_aware(tmp_date_str)

                tmp = network.get("code")
                if tmp is not None:
                    network_wrapper.code = self.validate_string(tmp)

                for station in network.findall(".mw:Station", namespaces=NSMAP):
                    stat_wrapper = StationWrapper()

                    tmp = station.get("code")
                    if tmp is not None:
                        stat_wrapper.code = self.validate_string(tmp)
                    else:
                        self.log_warning(
                            "Station with no code received \
                            when discovering network stations! Network: {0}".format(
                                vars(network_wrapper)
                            )
                        )
                        continue

                    tmp = station.find(".//mw:Latitude", namespaces=NSMAP)
                    if tmp is not None:
                        stat_wrapper.latitude = self.validate_string(tmp.text)

                    tmp = station.find(".//mw:Longitude", namespaces=NSMAP)
                    if tmp is not None:
                        stat_wrapper.longitude = self.validate_string(tmp.text)

                    tmp = station.find(".//mw:Elevation", namespaces=NSMAP)
                    if tmp is not None:
                        stat_wrapper.elevation = self.validate_string(tmp.text)

                    tmp = station.get("restrictedStatus")
                    if tmp is not None:
                        stat_wrapper.restricted_status = self.validate_string(tmp)

                    tmp = station.get("startDate")
                    if tmp is not None:
                        tmp_date_str = self.validate_string(tmp)
                        stat_wrapper.start_date = self.make_dt_str_aware(tmp_date_str)

                    tmp = station.get("endDate")
                    if tmp is not None:
                        tmp_date_str = self.validate_string(tmp)
                        stat_wrapper.end_date = self.make_dt_str_aware(tmp_date_str)

                    tmp = station.find(".//mw:CreationDate", namespaces=NSMAP)
                    if tmp is not None:
                        tmp_date_str = self.validate_string(tmp.text)
                        stat_wrapper.creation_date = self.make_dt_str_aware(tmp_date_str)
                    else:
                        # TODO: creation_date should be nullable in the DB
                        stat_wrapper.creation_date = self.make_dt_str_aware("1980-01-01T00:00:00")

                    tmp = station.find(".//mw:Site//mw:Name", namespaces=NSMAP)
                    if tmp is not None:
                        stat_wrapper.site_name = self.validate_string(tmp.text)

                    yield node_wrapper, network_wrapper, stat_wrapper
        except ParseError:
            self.log_exception()
        except:
            self.log_exception()
            raise

    def _save_network_station(self, node_wrapper, network_wrapper, station_wrapper):
        try:
            stat = self.get_station_if_known(network_wrapper, station_wrapper)

            # If station is known in the database, just update it with the
            # latest FDSN data, otherwise add it to the database
            if stat:
                # stat.code = station_wrapper.code
                stat.latitude = station_wrapper.latitude
                stat.longitude = station_wrapper.longitude
                stat.elevation = station_wrapper.elevation
                stat.restricted_status = station_wrapper.restricted_status
                # stat.start_date = station_wrapper.start_date
                stat.end_date = station_wrapper.end_date
                stat.creation_date = station_wrapper.creation_date
                stat.site_name = station_wrapper.site_name
                stat.save()
                stat.ext_basic_data.last_synced = timezone.now()
                stat.ext_basic_data.save()
            else:
                self.log_information(
                    "Adding: node {0} Network {1} Year {2} Station {3} Year {4}".format(
                        node_wrapper.code,
                        network_wrapper.code,
                        network_wrapper.parse_start_date_year(),
                        station_wrapper.code,
                        station_wrapper.parse_start_date_year(),
                    )
                )

                # Create station entity
                stat = FdsnStation()
                # Assign station to network
                stat.fdsn_network = FdsnNetwork.objects.get(
                    fdsn_node__code=node_wrapper.code,
                    code=network_wrapper.code,
                    start_date__year=network_wrapper.parse_start_date_year(),
                )
                # Fill data obtained from the Web Service
                stat.code = station_wrapper.code
                stat.latitude = station_wrapper.latitude
                stat.longitude = station_wrapper.longitude
                stat.elevation = station_wrapper.elevation
                stat.restricted_status = station_wrapper.restricted_status
                stat.start_date = station_wrapper.start_date
                stat.end_date = station_wrapper.end_date
                stat.creation_date = station_wrapper.creation_date
                stat.site_name = station_wrapper.site_name

                # Create ext entities and assign fields that will be later
                # used to restore the references during sync
                ext_basic = self.get_ext_if_known(
                    ExtBasicData, network_wrapper, station_wrapper
                )
                if not ext_basic:
                    ext_basic = ExtBasicData()
                    ext_basic.ext_network_code = network_wrapper.code
                    ext_basic.ext_network_start_year = (
                        network_wrapper.parse_start_date_year()
                    )
                    ext_basic.ext_station_code = station_wrapper.code
                    ext_basic.ext_station_start_year = (
                        station_wrapper.parse_start_date_year()
                    )

                ext_owner = self.get_ext_if_known(
                    ExtOwnerData, network_wrapper, station_wrapper
                )
                if not ext_owner:
                    ext_owner = ExtOwnerData()
                    ext_owner.ext_network_code = network_wrapper.code
                    ext_owner.ext_network_start_year = (
                        network_wrapper.parse_start_date_year()
                    )
                    ext_owner.ext_station_code = station_wrapper.code
                    ext_owner.ext_station_start_year = (
                        station_wrapper.parse_start_date_year()
                    )

                ext_morphology = self.get_ext_if_known(
                    ExtMorphologyData, network_wrapper, station_wrapper
                )
                if not ext_morphology:
                    ext_morphology = ExtMorphologyData()
                    ext_morphology.ext_network_code = network_wrapper.code
                    ext_morphology.ext_network_start_year = (
                        network_wrapper.parse_start_date_year()
                    )
                    ext_morphology.ext_station_code = station_wrapper.code
                    ext_morphology.ext_station_start_year = (
                        station_wrapper.parse_start_date_year()
                    )

                ext_housing = self.get_ext_if_known(
                    ExtHousingData, network_wrapper, station_wrapper
                )
                if not ext_housing:
                    ext_housing = ExtHousingData()
                    ext_housing.ext_network_code = network_wrapper.code
                    ext_housing.ext_network_start_year = (
                        network_wrapper.parse_start_date_year()
                    )
                    ext_housing.ext_station_code = station_wrapper.code
                    ext_housing.ext_station_start_year = (
                        station_wrapper.parse_start_date_year()
                    )

                ext_borehole = self.get_ext_if_known(
                    ExtBoreholeData, network_wrapper, station_wrapper
                )
                if not ext_borehole:
                    ext_borehole = ExtBoreholeData()
                    ext_borehole.ext_network_code = network_wrapper.code
                    ext_borehole.ext_network_start_year = (
                        network_wrapper.parse_start_date_year()
                    )
                    ext_borehole.ext_station_code = station_wrapper.code
                    ext_borehole.ext_station_start_year = (
                        station_wrapper.parse_start_date_year()
                    )

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
                except Exception:
                    self.log_exception()
                    raise

                # Restore the references between this station and photos that
                # have been already uploaded for it in the past
                Photo.objects.filter(
                    ext_network_code=network_wrapper.code,
                    ext_network_start_year=network_wrapper.parse_start_date_year(),
                    ext_station_code=station_wrapper.code,
                    ext_station_start_year=station_wrapper.parse_start_date_year(),
                ).update(fdsn_station=stat)

                # Restore the references between this station and
                # past access information
                ExtAccessData.objects.filter(
                    ext_network_code=network_wrapper.code,
                    ext_network_start_year=network_wrapper.parse_start_date_year(),
                    ext_station_code=station_wrapper.code,
                    ext_station_start_year=station_wrapper.parse_start_date_year(),
                ).update(fdsn_station=stat)
        except FdsnNetwork.DoesNotExist:
            self.log_exception(
                "Network is not known! Node: {0} Network: {1} Station: {2}".format(
                    vars(node_wrapper), vars(network_wrapper), vars(station_wrapper)
                )
            )
            # raise
        except Exception:
            self.log_exception(
                "Node: {0} Network: {1} Station: {2}".format(
                    vars(node_wrapper), vars(network_wrapper), vars(station_wrapper)
                )
            )
            # raise

    def _sync_fdsn_stations(self):
        try:
            for network_code in self._get_fdsn_networks():
                for url, param_wrapper in self._discover_network_routes(network_code):
                    for (
                        node_wrapper,
                        network_wrapper,
                        stat_wrapper,
                    ) in self._discover_network_stations(url, param_wrapper):
                        self._save_network_station(
                            node_wrapper, network_wrapper, stat_wrapper
                        )
        except Exception:
            self.log_exception()
            raise


class FdsnManager(StationBookLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()
        self.fdsn_netman = FdsnNetworkManager()
        self.fdsn_routman = FdsnRoutingManager()

    def process_fdsn(self):
        try:
            self.log_information("Flushing stations...")
            FdsnStation.objects.all().delete()
            self.log_information("FDSN sync started!")
            self.fdsn_netman._sync_fdsn_networks()
            self.fdsn_routman._sync_fdsn_stations()
            self.log_information("FDSN sync completed!")
        except KeyboardInterrupt:
            self.log_exception("FDSN sync interrupted manually!")

    def process_fdsn_in_thread(self):
        worker = BackgroundThread(self.process_fdsn())
        worker.run()
