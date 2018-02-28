from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import FdsnStation, \
ExtBasicData, ExtOwnerData, ExtMorphologyData, ExtHousingData, ExtAccessData, \
ExtBoreholeData, ExtBoreholeLayerData, Photo

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_delete, sender=FdsnStation)
def fdsn_station_pre_delete(sender, instance, using, **kwargs):
    ExtBasicData.objects.filter(station__pk=instance.pk).delete()
    ExtOwnerData.objects.filter(station__pk=instance.pk).delete()
    ExtMorphologyData.objects.filter(station__pk=instance.pk).delete()
    ExtHousingData.objects.filter(station__pk=instance.pk).delete()
    ExtBoreholeLayerData.objects.filter(borehole_data__station__pk=instance.pk).delete()
    ExtBoreholeData.objects.filter(station__pk=instance.pk).delete()

    ExtAccessData.objects.filter(fdsn_station__pk=instance.pk).delete()
    Photo.objects.filter(fdsn_station__pk=instance.pk).delete()