from .models import Chat

from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(m2m_changed, sender=Chat.users.through)
def m2m_changed_update_members_count(sender, instance, action, *args, **kwargs):
    #instance.users.add(instance.admin.id)
    if action == "post_add":
        instance.members_count = instance.users.all().count()
        #instance.users.add(instance.admin.id)
        instance.save()