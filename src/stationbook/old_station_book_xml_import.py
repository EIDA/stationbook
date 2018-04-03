import sys, os, django
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stationbook.settings")
django.setup()

from book.models import \
FdsnStation, ExtOwnerData, ExtMorphologyData, ExtHousingData
import xml.etree.ElementTree as ET

class SB1XMLProcessor(object):
    xml_root = None

    def xml_load(self):
        try:
            self.xml_root = ET.parse('/nobackup/users/bienkows/stationbookdata/sb_export.xml').getroot()
        except:
            raise
    
    def get_housing_class_code(self, hc):
        if not hc: return ''
        elif hc.lower() == 'free field': return 'free_field'
        elif hc.lower() == 'urban free field': return 'urban_free_field'
        elif hc.lower() == 'underground shelter': return 'underground_shelter'
        elif hc.lower() == 'building': return 'building'
        elif hc.lower() == 'otherstructure': return 'other_structure'
        elif hc.lower() == 'cave': return 'cave'
        elif hc.lower() == 'tunnel': return 'tunnel'
        elif hc.lower() == 'borehole': return 'borehole'
        elif 'cave' in hc.lower(): return 'cave'
        elif 'tunnel' in hc.lower(): return 'tunnel'
        else: return ''

    def get_morphology_class(self, mc):
        if not mc: return 'unknown'
        elif mc.lower() == 't1': return 't1'
        elif mc.lower() == 't2': return 't2'
        elif mc.lower() == 't3': return 't3'
        elif mc.lower() == 't4': return 't4'
        else: return 'unknown'
    
    def get_ground_type_ec8(self, gt):
        if not gt: return 'unknown'
        elif gt.lower() == 'a': return ''
        elif gt.lower() == 'b': return ''
        elif gt.lower() == 'c': return ''
        elif gt.lower() == 'd': return ''
        elif gt.lower() == 'e': return ''
        elif gt.lower() == 's1': return ''
        elif gt.lower() == 's2': return ''
        else: return 'unknown'

    def get_geological_unit(self, gu):
        if not gu: return 'unknown'
        elif gu.lower() == 'alluvial deposits': return 'alluvial_deposits'
        elif gu.lower() == 'alluvial terraces': return 'ancient_alluvialterraces'
        elif gu.lower() == 'ancient alluvial terraces': return 'ancient_alluvialterraces'
        elif gu.lower() == 'clay': return 'clay'
        elif gu.lower() == 'clay, sand': return 'clay'
        elif gu.lower() == 'conglomerate': return 'conglomerate'
        elif gu.lower() == 'debris': return 'debris'
        elif gu.lower() == 'dolomite': return 'dolomite'
        elif gu.lower() == 'fluvial deposits': return 'fluvial_deposits'
        elif gu.lower() == 'gneiss': return 'gneiss'
        elif gu.lower() == 'granite': return 'granite'
        elif gu.lower() == 'limestone': return 'limestone'
        elif gu.lower() == 'metamorphic rock': return 'metamorphic_rock'
        elif gu.lower() == 'sand': return 'sand_deposits'
        elif gu.lower() == 'sand deposits': return 'sand_deposits'
        elif gu.lower() == 'sandstone': return 'sandstone'
        elif gu.lower() == 'schist': return 'schist'
        elif gu.lower() == 'thin loess above triassic limestone': return 'limestone'
        elif gu.lower() == 'volcanic rocks': return 'volcanic_rocks'
        else: return 'unknown'
    
    def yes_no_to_bool(self, yn):
        if not yn: return False
        elif yn.lower() == 'yes': return True
        else: return False
    
    def float_to_int(self, i):
        try:
            return int(i)
        except:
            return 0
    
    def process_entries(self):
        try:
            for e in self.xml_root.findall('.//DATA_RECORD'):
                stationOwnerReference_resourceID = e.find('.//stationOwnerReference_resourceID').text
                tmp = stationOwnerReference_resourceID.split('/')

                network_start_year = tmp[3][0:4]
                station_start_year = tmp[5][0:4]

                network_code = e.find('.//networkCode').text
                station_code = e.find('.//stationCode').text

                siteMorphology_morphology = e.find('.//siteMorphology_morphology').text
                siteMorphology_geologicalUnit = e.find('.//siteMorphology_geologicalUnit').text
                siteMorphology_siteClassDescription = e.find('.//siteMorphology_siteClassDescription').text
                siteMorphology_siteClassEC8 = e.find('.//siteMorphology_siteClassEC8').text

                inBuilding = e.find('.//inBuilding').text
                housingClass = e.find('.//housingClass').text
                housingDescription = e.find('.//housingDescription').text
                distanceToBuilding_value = e.find('.//distanceToBuilding_value').text

                owner_address = e.find('.//owner_address').text
                owner_agency = e.find('.//owner_agency').text
                owner_department = e.find('.//owner_department').text
                owner_email = e.find('.//owner_email').text
                owner_forename = e.find('.//owner_forename').text
                owner_name = e.find('.//owner_name').text
                owner_phone = e.find('.//owner_phone').text

                print('{} {} {} {}'.format(
                    network_code,
                    network_start_year,
                    station_code,
                    station_start_year
                ))

                stat = None
                try:
                    stat = FdsnStation.objects.get(
                        fdsn_network__code=network_code,
                        fdsn_network__start_date__year=network_start_year,
                        code=station_code,
                        start_date__year=station_start_year)
                except FdsnStation.DoesNotExist:
                    try:
                        stat = FdsnStation.objects.get(
                            fdsn_network__code=network_code,
                            code=station_code)
                    except:
                        continue
                
                owner = ExtOwnerData.objects.get(station__pk=stat.pk)
                owner.street = owner_address or 'n/a'
                owner.agency = owner_agency or 'n/a'
                owner.department = owner_department or 'n/a'
                owner.email = owner_email or 'n/a'
                owner.name_first = owner_forename or 'n/a'
                owner.name_last = owner_name or 'n/a'
                owner.phone = owner_phone or 'n/a'
                owner.save()

                morph = ExtMorphologyData.objects.get(station__pk=stat.pk)
                morph.description = siteMorphology_siteClassDescription or 'n/a'
                morph.morphology_class = self.get_morphology_class(siteMorphology_morphology)
                morph.geological_unit = self.get_geological_unit(siteMorphology_geologicalUnit)
                morph.ground_type_ec8 = self.get_ground_type_ec8(siteMorphology_siteClassEC8)
                morph.save()

                housing = ExtHousingData.objects.get(station__pk=stat.pk)
                housing.in_building = self.yes_no_to_bool(inBuilding)
                housing.housing_class = self.get_housing_class_code(housingClass)
                housing.description = housingDescription or 'n/a'
                housing.distance_to_building = self.float_to_int(distanceToBuilding_value)
                housing.save()

                print(stat.site_name)
        except:
            raise

if __name__ == '__main__':
    try:
        worker = SB1XMLProcessor()
        worker.xml_load()
        worker.process_entries()
    except:
        raise