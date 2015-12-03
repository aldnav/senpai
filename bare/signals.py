
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification, Client


@receiver(post_save, sender=Notification)
def ping_apn_for_notif(sender, instance, created, **kwargs):
    if created:
        clients = Client.objects.filter(owner=instance.owner)\
                        .values_list('registration_id', flat=True)
        requests.get('http://localhost:8888/',
                     params={'client': clients, 'context': instance.id})
        # fallback if user was offline
