from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from .utils import distribute_smart_share


@receiver(post_save, sender=User)
def smart_share_signal(sender, instance, created, **kwargs):

    if created and instance.referred_by:

        distribute_smart_share(instance)